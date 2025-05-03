import os
from pyworkflow.protocol.params import PointerParam
from pwem.protocols import EMProtocol
from pwchem.objects import SetOfSmallMolecules
from pwem.objects.data import AtomStruct
from pafnucy import Plugin
from pwchem.utils import *
import pyworkflow.object as pwobj

class ProtChemPafnuncy (EMProtocol):
    """ Protocol to prepare and predict ligand and protein structures with Pafnuncy."""

    _label = 'Pafnuncy ligand-target predictions'

    def __init__(self, **kwargs):
        EMProtocol.__init__(self, **kwargs)

    def _defineParams(self, form):
        form.addSection(label='Input')

        form.addParam('inputSet', PointerParam, pointerClass= "SetOfSmallMolecules",
                      label='Set of ligands:', allowsNull=False,
                      help='Select the set of small molecules (ligands) for preparation and prediction.')

        form.addParam('inputPockets', PointerParam, pointerClass= "AtomStruct",
                      label='Target protein', allowsNull=False,
                      help='Select the atomic structure for preparation and prediction.')

    def _insertAllSteps(self):
        self._insertFunctionStep('runPreparation')
        self._insertFunctionStep('runPrediction')

    def runPreparation(self):
        inputMoleculeSet = self.inputSet.get()
        inputPocketSet = os.path.abspath(self.inputPockets.get().getFileName())
        
        ligands = [os.path.abspath(mol.getFileName()) for mol in inputMoleculeSet]
        
        if not ligands:
            raise RuntimeError("No ligands found. Check your input.")
        
        
        output_file = os.path.abspath(self._getExtraPath("complexes.hdf"))
        
        ligands_list = ligands[:1000] 
        ligands_str = ' '.join(ligands_list) 
        ligand_ext = os.path.splitext(ligands[0])[-1][1:] if ligands else 'mol2'
        pocket_ext = os.path.splitext(inputPocketSet)[1][1:] if inputPocketSet else 'mol2'
        
        
        args = f"-l {ligands_str} --ligand_format {ligand_ext} -p {inputPocketSet} --pocket_format {pocket_ext} -o {output_file}"
        print(f"Executing prepare.py with {len(ligands_list)} ligands.")
        Plugin.runPafnuncy(f'python prepare.py', args)


    def runPrediction(self):
        complexes_file = os.path.abspath(self._getExtraPath("complexes.hdf"))
        output_predictions = os.path.abspath(self._getExtraPath("predictions.csv"))
        
        args = f"-i {complexes_file} -o {output_predictions}"
        Plugin.runPafnuncy(f' python predict.py', args)

        updatedMoleculeSet = self.inputSet.get().createCopy(self._getPath(), copyInfo=True)
        
        with open(output_predictions) as f:
            header = f.readline().strip().split(',') 
            predictions = [dict(zip(header, line.strip().split(','))) for line in f]
        
        proteinFile=self.inputPockets.get().getFileName()
        
        for result in predictions:
            ligand_name, pKd_value = result['name'], result['prediction']
            for mol in self.inputSet.get():
                if ligand_name == mol.getMolName():
                    setattr(mol, 'Predicted_pKa_Pafnucy', pwobj.Float(pKd_value))
                    setattr(mol,'proteinFile',pwobj.String(proteinFile))
                    updatedMoleculeSet.append(mol.clone())
            
        self._defineOutputs(updatedMoleculeSet=updatedMoleculeSet)
