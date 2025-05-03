
#### VERÓNICA GAMO ######

from pafnucy.protocols.protocol_pafnucy import ProtChemPafnuncy
from pyworkflow.tests import BaseTest, setupTestProject, DataSet
from pwchem.protocols import ProtChemImportSmallMolecules
from pwem.protocols import ProtImportPdb
from pwchem.utils import assertHandle


class TestPafnucyPrediction(BaseTest):
    @classmethod
    def setUpClass(cls):
        cls.ds = DataSet.getDataSet('model_building_tutorial')
        cls.dsLig = DataSet.getDataSet('smallMolecules')
        setupTestProject(cls)

        cls._runImportPDB()
        cls._runImportSmallMols()
        cls._waitOutput(cls.protImportPDB, 'outputPdb', sleepTime=5)
        cls._waitOutput(cls.protImportSmallMols, 'outputSmallMolecules', sleepTime=5)

    @classmethod
    def _runImportPDB(cls):
        cls.protImportPDB = cls.newProtocol(
            ProtImportPdb,
            inputPdbData=1,
            pdbFile=cls.ds.getFile('PDBx_mmCIF/5ni1.pdb')
        )
        cls.proj.launchProtocol(cls.protImportPDB, wait=False)

    @classmethod
    def _runImportSmallMols(cls):
        cls.protImportSmallMols = cls.newProtocol(
            ProtChemImportSmallMolecules,
            filesPath=cls.dsLig.getFile('mol2')
        )
        cls.proj.launchProtocol(cls.protImportSmallMols, wait=False)

    def _runPafnucyPrediction(self):
        protPafnucy = self.newProtocol(
            ProtChemPafnuncy,
            inputSet=self.protImportSmallMols.outputSmallMolecules,
            inputPockets=self.protImportPDB.outputPdb
        )
        self.proj.launchProtocol(protPafnucy, wait=True)
        return protPafnucy

    def test(self):
        pPafnucy = self._runPafnucyPrediction()
        self._waitOutput(pPafnucy, 'updatedMoleculeSet', sleepTime=10)
        assertHandle(self.assertIsNotNone, getattr(pPafnucy, 'updatedMoleculeSet', None), cwd=pPafnucy.getWorkingDir())
