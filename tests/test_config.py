"""Script to test the config module of the PhysiCOOL package."""
import unittest
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from physicool import config

CONFIG_PATH = Path("PhysiCell/config/settings_read_only.xml")
WRITE_PATH = Path("test.xml")

EXPECTED_DOMAIN_READ = {
    "x_min": -500.0,
    "x_max": 500.0,
    "y_min": -500.0,
    "y_max": 500.0,
    "z_min": -10.0,
    "z_max": 10.0,
    "dx": 20.0,
    "dy": 20.0,
    "dz": 20.0,
    "use_2d": True,
}

EXPECTED_DOMAIN_WRITE = {
    "x_min": -200.0,
    "x_max": 200.0,
    "y_min": -500.0,
    "y_max": 500.0,
    "z_min": -10.0,
    "z_max": 10.0,
    "dx": 20.0,
    "dy": 20.0,
    "dz": 20.0,
    "use_2d": False,
}

EXPECTED_OVERALL_READ = {
    "max_time": 620.0,
    "dt_diffusion": 0.01,
    "dt_mechanics": 0.1,
    "dt_phenotype": 6.0,
}

EXPECTED_OVERALL_WRITE = {
    "max_time": 120.0,
    "dt_diffusion": 0.01,
    "dt_mechanics": 0.1,
    "dt_phenotype": 6.0,
}

EXPECTED_SUBSTANCE_READ = {
    "name": "substrate",
    "diffusion_coefficient": 100000.0,
    "decay_rate": 10.0,
    "initial_condition": 0.0,
    "dirichlet_boundary_condition": 0.0,
}

EXPECTED_SUBSTANCE_WRITE = {
    "name": "substrate",
    "diffusion_coefficient": 400.0,
    "decay_rate": 1.0,
    "initial_condition": 0.0,
    "dirichlet_boundary_condition": 0.0,
}

EXPECTED_CYCLE_DURATIONS_READ = {
    "code": 6.0,
    "phase_durations": [300.0, 480.0, 240.0, 60.0],
    "phase_transition_rates": None,
}

EXPECTED_CYCLE_DURATIONS_WRITE = {
    "code": 6.0,
    "phase_durations": [100.0, 10.0, 240.0, 60.0],
    "phase_transition_rates": None,
}

EXPECTED_CYCLE_RATES_READ = {
    "code": 6.0,
    "phase_durations": None,
    "phase_transition_rates": [0.00334672, 0.00208333, 0.00416667, 0.0166667],
}

EXPECTED_CYCLE_RATES_WRITE = {
    "code": 6.0,
    "phase_durations": None,
    "phase_transition_rates": [0.001, 0.001, 0.00416667, 0.0166667],
}

EXPECTED_DEATH_APOPTOSIS_READ = {
    "code": 100.0,
    "death_rate": 5.31667e-05,
    "phase_durations": [516],
    "phase_transition_rates": None,
    "unlysed_fluid_change_rate": 0.05,
    "lysed_fluid_change_rate": 0.0,
    "cytoplasmic_biomass_change_rate": 1.66667e-02,
    "nuclear_biomass_change_rate": 5.83333e-03,
    "calcification_rate": 0.0,
    "relative_rupture_volume": 2.0,
}

EXPECTED_DEATH_APOPTOSIS_WRITE = {
    "code": 100.0,
    "death_rate": 5.31667e-05,
    "phase_durations": [518],
    "phase_transition_rates": None,
    "unlysed_fluid_change_rate": 0.05,
    "lysed_fluid_change_rate": 0.0,
    "cytoplasmic_biomass_change_rate": 1.66667e-02,
    "nuclear_biomass_change_rate": 5.83333e-03,
    "calcification_rate": 0.5,
    "relative_rupture_volume": 2.0,
}

EXPECTED_DEATH_NECROSIS_READ = {
    "code": 101.0,
    "death_rate": 0.0,
    "phase_durations": [0.0, 86400],
    "phase_transition_rates": None,
    "unlysed_fluid_change_rate": 0.05,
    "lysed_fluid_change_rate": 0.0,
    "cytoplasmic_biomass_change_rate": 1.66667e-02,
    "nuclear_biomass_change_rate": 5.83333e-03,
    "calcification_rate": 0.0,
    "relative_rupture_volume": 2.0,
}

EXPECTED_VOLUME_READ = {
    "total": 2494.0,
    "fluid_fraction": 0.75,
    "nuclear": 540.0,
    "fluid_change_rate": 0.05,
    "cytoplasmic_biomass_change_rate": 0.0045,
    "nuclear_biomass_change_rate": 0.0055,
    "calcified_fraction": 0.0,
    "calcification_rate": 0.0,
    "relative_rupture_volume": 2.0,
}

EXPECTED_VOLUME_WRITE = {
    "total": 2494.0,
    "fluid_fraction": 0.75,
    "nuclear": 100.0,
    "fluid_change_rate": 0.05,
    "cytoplasmic_biomass_change_rate": 0.0045,
    "nuclear_biomass_change_rate": 0.0055,
    "calcified_fraction": 0.5,
    "calcification_rate": 1.0,
    "relative_rupture_volume": 3.0,
}

EXPECTED_MOTILITY_READ = {
    "speed": 1.0,
    "persistence_time": 1.0,
    "migration_bias": 0.5,
    "motility_enabled": False,
    "use_2d": True,
    "chemotaxis_enabled": False,
    "chemotaxis_substrate": "substrate",
    "chemotaxis_direction": 1.0,
}

EXPECTED_MOTILITY_WRITE = {
    "speed": 12.0,
    "persistence_time": 60.0,
    "migration_bias": 0.5,
    "motility_enabled": True,
    "use_2d": True,
    "chemotaxis_enabled": False,
    "chemotaxis_substrate": "substrate",
    "chemotaxis_direction": 1.0,
}

EXPECTED_MECHANICS_READ = {
    "cell_cell_adhesion_strength": 0.4,
    "cell_cell_repulsion_strength": 10.0,
    "relative_maximum_adhesion_distance": 1.25,
    "set_relative_equilibrium_distance": 1.8,
    "set_absolute_equilibrium_distance": 15.12,
}

EXPECTED_MECHANICS_WRITE = {
    "cell_cell_adhesion_strength": 4.0,
    "cell_cell_repulsion_strength": 100.0,
    "relative_maximum_adhesion_distance": 1.25,
    "set_relative_equilibrium_distance": 1.8,
    "set_absolute_equilibrium_distance": 15.12,
}

EXPECTED_SECRETION_READ_SUBSTRATE = {
    "name": "substrate",
    "secretion_rate": 0.0,
    "secretion_target": 1.0,
    "uptake_rate": 0.0,
    "net_export_rate": 0.0,
}

EXPECTED_SECRETION_READ_OXYGEN = {
    "name": "oxygen",
    "secretion_rate": 0.0,
    "secretion_target": 1.0,
    "uptake_rate": 0.0,
    "net_export_rate": 0.0,
}

EXPECTED_SECRETION_READ = [
    EXPECTED_SECRETION_READ_SUBSTRATE,
    EXPECTED_SECRETION_READ_OXYGEN,
]

EXPECTED_CUSTOM_READ = [{"name": "sample", "value": 1.0}]
EXPECTED_CUSTOM_WRITE = [{"name": "sample", "value": 5.0}]

EXPECTED_USER_PARAMETERS_READ = [
    {"name": "random_seed", "value": 0.0},
    {"name": "number_of_cells", "value": 5.0},
]

EXPECTED_USER_PARAMETERS_WRITE = [
    {"name": "random_seed", "value": 1.0},
    {"name": "number_of_cells", "value": 5.0},
]


class ReadDataTest(unittest.TestCase):
    def setUp(self):
        self.tree = ElementTree.parse(CONFIG_PATH)

    def test_parse_domain(self):
        data = config.parse_domain(tree=self.tree, path="domain")
        self.assertEqual(EXPECTED_DOMAIN_READ, data)

    def test_parse_overall(self):
        data = config.parse_overall(tree=self.tree, path="overall")
        self.assertEqual(EXPECTED_OVERALL_READ, data)

    def test_parse_substance(self):
        data = config.parse_substance(
            tree=self.tree, path="microenvironment_setup", name="substrate"
        )
        self.assertEqual(EXPECTED_SUBSTANCE_READ, data)

    def test_parse_me(self):
        data = config.parse_microenvironment(
            tree=self.tree, path="microenvironment_setup"
        )
        self.assertEqual([EXPECTED_SUBSTANCE_READ], data)

    def test_parse_cycle_durations(self):
        data = config.parse_cycle(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_DURATIONS_READ, data)

    def test_parse_cycle_rates(self):
        data = config.parse_cycle(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='cancer']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_RATES_READ, data)

    def test_parse_death_model(self):
        data = config.parse_death_model(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/death",
            name="apoptosis",
        )
        self.assertEqual(EXPECTED_DEATH_APOPTOSIS_READ, data)

    def test_parse_volume(self):
        data = config.parse_volume(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/volume",
        )
        self.assertEqual(EXPECTED_VOLUME_READ, data)

    def test_parse_mechanics(self):
        data = config.parse_mechanics(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/mechanics",
        )
        self.assertEqual(EXPECTED_MECHANICS_READ, data)

    def test_parse_motility(self):
        data = config.parse_motility(
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/motility",
        )
        self.assertEqual(EXPECTED_MOTILITY_READ, data)


class WriteDataTest(unittest.TestCase):
    def setUp(self) -> None:
        copyfile(CONFIG_PATH, WRITE_PATH)
        self.tree = ElementTree.parse(WRITE_PATH)

    def test_write_domain(self):
        config.write_domain(
            new_values=EXPECTED_DOMAIN_WRITE,
            tree=self.tree,
            path="domain",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        domain_data = config.parse_domain(
            tree=new_tree,
            path="domain",
        )
        self.assertEqual(EXPECTED_DOMAIN_WRITE, domain_data)

    def test_write_overall(self):
        config.write_overall(
            new_values=EXPECTED_OVERALL_WRITE,
            tree=self.tree,
            path="overall",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        overall_data = config.parse_overall(
            tree=new_tree,
            path="overall",
        )
        self.assertEqual(EXPECTED_OVERALL_WRITE, overall_data)

    def test_write_substance(self):
        config.write_substance(
            new_values=EXPECTED_SUBSTANCE_WRITE,
            tree=self.tree,
            path="microenvironment_setup",
            name="substrate",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        substance_data = config.parse_substance(
            tree=new_tree, path="microenvironment_setup", name="substrate"
        )
        self.assertEqual(EXPECTED_SUBSTANCE_WRITE, substance_data)

    def test_write_cycle_durations(self):
        config.write_cycle(
            new_values=EXPECTED_CYCLE_DURATIONS_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/cycle",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        cycle_data = config.parse_cycle(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_DURATIONS_WRITE, cycle_data)

    def test_write_cycle_rates(self):
        config.write_cycle(
            new_values=EXPECTED_CYCLE_RATES_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='cancer']/phenotype/cycle",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        cycle_data = config.parse_cycle(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='cancer']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_RATES_WRITE, cycle_data)

    def test_write_death_model_durations(self):
        config.write_death_model(
            new_values=EXPECTED_DEATH_APOPTOSIS_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/death",
            name="apoptosis",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        death_data = config.parse_death_model(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/death",
            name="apoptosis"
        )
        self.assertEqual(EXPECTED_DEATH_APOPTOSIS_WRITE, death_data)

    def test_write_volume(self):
        config.write_volume(
            new_values=EXPECTED_VOLUME_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/volume",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        volume_data = config.parse_volume(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/volume",
        )
        self.assertEqual(EXPECTED_VOLUME_WRITE, volume_data)

    def test_write_mechanics(self):
        config.write_mechanics(
            new_values=EXPECTED_MECHANICS_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/mechanics",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        mechanics_data = config.parse_mechanics(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/mechanics",
        )
        self.assertEqual(EXPECTED_MECHANICS_WRITE, mechanics_data)

    def test_write_motility(self):
        config.write_motility(
            new_values=EXPECTED_MOTILITY_WRITE,
            tree=self.tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/motility",
        )
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        motility_data = config.parse_motility(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/phenotype/motility",
        )
        self.assertEqual(EXPECTED_MOTILITY_WRITE, motility_data)

    def test_write_custom_cell(self):
        config.write_custom_data(new_values=EXPECTED_CUSTOM_WRITE, tree=self.tree,
                                 path=f"cell_definitions/cell_definition[@name='default']/custom_data")
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        custom_data = config.parse_custom(
            tree=new_tree,
            path=f"cell_definitions/cell_definition[@name='default']/custom_data"
        )
        self.assertEqual(EXPECTED_CUSTOM_WRITE, custom_data)

    def test_write_custom_user(self):
        config.write_custom_data(new_values=EXPECTED_USER_PARAMETERS_WRITE, tree=self.tree, path="user_parameters")
        self.tree.write(WRITE_PATH)

        new_tree = ElementTree.parse(WRITE_PATH)
        custom_data = config.parse_custom(
            tree=new_tree,
            path=f"user_parameters",
        )
        self.assertEqual(EXPECTED_USER_PARAMETERS_WRITE, custom_data)

    def tearDown(self) -> None:
        Path(WRITE_PATH).unlink()


class PhysiCellConfigTest(unittest.TestCase):
    def setUp(self):
        """Creates and stores a parser object to read data from the config file."""
        copyfile(CONFIG_PATH, WRITE_PATH)
        self.xml_data = config.ConfigFileParser(CONFIG_PATH)
        self.xml_write = config.ConfigFileParser(WRITE_PATH)

    def test_get_cell_definition_list(self):
        """Asserts that the cell definitions extracted from the config file are correct."""
        cell_list = self.xml_data.cell_definitions_list
        self.assertEqual(cell_list, ["default", "cancer"])

    def test_read_domain_params(self):
        """Asserts that the XML domain data was properly read into a Domain object."""
        expected_data = config.Domain(**EXPECTED_DOMAIN_READ)
        domain_data = self.xml_data.read_domain_params()
        self.assertEqual(expected_data, domain_data)

    def test_read_overall_params(self):
        expected_data = config.Overall(**EXPECTED_OVERALL_READ)
        overall_data = self.xml_data.read_overall_params()
        self.assertEqual(expected_data, overall_data)

    def test_read_me_params(self):
        expected_data = [config.Substance(**EXPECTED_SUBSTANCE_READ)]
        me_data = self.xml_data.read_me_params()
        self.assertEqual(expected_data, me_data)

    def test_read_cycle_durations_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_data = config.Cycle(**EXPECTED_CYCLE_DURATIONS_READ)
        cycle_data = self.xml_data.read_cycle_params("default")
        self.assertEqual(expected_data, cycle_data)

    def test_read_cycle_rates_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_data = config.Cycle(**EXPECTED_CYCLE_RATES_READ)
        cycle_data = self.xml_data.read_cycle_params("cancer")
        self.assertEqual(expected_data, cycle_data)

    def test_read_death(self):
        expected_data = [
            config.Death(**EXPECTED_DEATH_APOPTOSIS_READ),
            config.Death(**EXPECTED_DEATH_NECROSIS_READ),
        ]
        death_data = self.xml_data.read_death_params("default")
        self.assertEqual(expected_data, death_data)

    def test_read_volume_params(self):
        """Asserts that the volume parameters extracted from the config file are correct."""
        expected_data = config.Volume(**EXPECTED_VOLUME_READ)
        volume_data = self.xml_data.read_volume_params("default")
        self.assertEqual(expected_data, volume_data)

    def test_read_mechanics_params(self):
        """Asserts that the mechanics parameters extracted from the config file are correct."""
        expected_data = config.Mechanics(**EXPECTED_MECHANICS_READ)
        mechanics_data = self.xml_data.read_mechanics_params("default")
        self.assertEqual(expected_data, mechanics_data)

    def test_read_motility_params(self):
        """Asserts that the motility parameters extracted from the config file are correct."""
        expected_data = config.Motility(**EXPECTED_MOTILITY_READ)
        motility_data = self.xml_data.read_motility_params("default")
        self.assertEqual(expected_data, motility_data)

    def test_read_secretion_params(self):
        """Asserts that the secretion parameters extracted from the config file are correct."""
        expected_data = [
            config.Secretion(**EXPECTED_SECRETION_READ_SUBSTRATE),
            config.Secretion(**EXPECTED_SECRETION_READ_OXYGEN),
        ]
        secretion_data = self.xml_data.read_secretion_params("default")
        self.assertEqual(expected_data, secretion_data)

    def test_read_custom_params(self):
        expected_data = [config.CustomData(**custom) for custom in EXPECTED_CUSTOM_READ]
        custom_data = self.xml_data.read_custom_data("default")
        self.assertEqual(expected_data, custom_data)

    def test_read_user_parameters(self):
        expected_data = [
            config.CustomData(**custom) for custom in EXPECTED_USER_PARAMETERS_READ
        ]
        user_data = self.xml_data.read_user_params()
        self.assertEqual(expected_data, user_data)

    def test_write_domain_params(self):
        """Asserts that Domain data is properly written to the XML file."""
        domain_data = self.xml_write.read_domain_params()
        domain_data.x_min = -200.0
        domain_data.x_max = 200.0
        domain_data.use_2d = False
        self.xml_write.write_domain_params(domain=domain_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        domain_data = config.parse_domain(
            tree=new_tree,
            path="domain",
        )
        self.assertEqual(EXPECTED_DOMAIN_WRITE, domain_data)

    def test_write_overall_params(self):
        """Asserts that overall data is properly written to the XML file."""
        overall_data = self.xml_write.read_overall_params()
        overall_data.max_time = 120.0
        self.xml_write.write_overall_params(overall=overall_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        overall_data = config.parse_overall(
            tree=new_tree,
            path="overall",
        )
        self.assertEqual(EXPECTED_OVERALL_WRITE, overall_data)

    def test_write_substance_params(self):
        """Asserts that overall data is properly written to the XML file."""
        substance_data = self.xml_write.read_me_params()
        substance_data[0].diffusion_coefficient = 400.0
        substance_data[0].decay_rate = 1.0
        self.xml_write.write_substance_params(substance=substance_data[0])

        new_tree = ElementTree.parse(WRITE_PATH)
        substance_data = config.parse_substance(
            tree=new_tree, path="microenvironment_setup", name="substrate"
        )
        self.assertEqual(EXPECTED_SUBSTANCE_WRITE, substance_data)

    def test_write_cycle_durations_params(self):
        cycle_data = self.xml_write.read_cycle_params("default")
        cycle_data.phase_durations = [100.0, 10.0, 240.0, 60.0]
        self.xml_write.write_cycle_params(name="default", cycle=cycle_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        cycle_data = config.parse_cycle(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_DURATIONS_WRITE, cycle_data)

    def test_write_cycle_rates_params(self):
        cycle_data = self.xml_write.read_cycle_params("cancer")
        cycle_data.phase_transition_rates = [0.001, 0.001, 0.00416667, 0.0166667]
        self.xml_write.write_cycle_params(name="cancer", cycle=cycle_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        cycle_data = config.parse_cycle(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='cancer']/phenotype/cycle",
        )
        self.assertEqual(EXPECTED_CYCLE_RATES_WRITE, cycle_data)

    def test_write_death_params(self):
        death_data = self.xml_write.read_death_params("default")
        death_data[0].phase_durations = [518.0]
        death_data[0].calcification_rate = 0.5
        self.xml_write.write_death_model_params(name="default", death=death_data[0], model_name="apoptosis")

        new_tree = ElementTree.parse(WRITE_PATH)
        death_data = config.parse_death_model(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/death",
            name="apoptosis"
        )
        self.assertEqual(EXPECTED_DEATH_APOPTOSIS_WRITE, death_data)

    def test_write_volume_params(self):
        volume_data = self.xml_write.read_volume_params("default")
        volume_data.nuclear = 100.0
        volume_data.calcified_fraction = 0.5
        volume_data.calcification_rate = 1.0
        volume_data.relative_rupture_volume = 3.0
        self.xml_write.write_volume_params(name="default", volume=volume_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        volume_data = config.parse_volume(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/volume",
        )
        self.assertEqual(EXPECTED_VOLUME_WRITE, volume_data)

    def test_write_mechanics_params(self):
        mechanics_data = self.xml_write.read_mechanics_params("default")
        mechanics_data.cell_cell_adhesion_strength = 4.0
        mechanics_data.cell_cell_repulsion_strength = 100.0
        self.xml_write.write_mechanics_params(name="default", mechanics=mechanics_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        mechanics_data = config.parse_mechanics(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/mechanics",
        )
        self.assertEqual(EXPECTED_MECHANICS_WRITE, mechanics_data)

    def test_write_motility_params(self):
        motility_data = self.xml_write.read_motility_params("default")
        motility_data.speed = 12.0
        motility_data.persistence_time = 60.0
        motility_data.motility_enabled = True
        self.xml_write.write_motility_params(name="default", motility=motility_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        motility_data = config.parse_motility(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/phenotype/motility",
        )
        self.assertEqual(EXPECTED_MOTILITY_WRITE, motility_data)

    def test_write_custom_params(self):
        custom_data = self.xml_write.read_custom_data("default")
        custom_data[0].value = 5.0
        self.xml_write.write_custom_params(name="default", custom_data=custom_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        custom_data = config.parse_custom(
            tree=new_tree,
            path="cell_definitions/cell_definition[@name='default']/custom_data",
        )
        self.assertEqual(EXPECTED_CUSTOM_WRITE, custom_data)

    def test_write_user_params(self):
        custom_data = self.xml_write.read_user_params()
        custom_data[0].value = 1.0
        custom_data[1].value = 5.0
        self.xml_write.write_user_params(custom_data=custom_data)

        new_tree = ElementTree.parse(WRITE_PATH)
        custom_data = config.parse_custom(
            tree=new_tree,
            path="user_parameters",
        )
        self.assertEqual(EXPECTED_USER_PARAMETERS_WRITE, custom_data)

    def tearDown(self) -> None:
        Path(WRITE_PATH).unlink()


if __name__ == "__main__":
    unittest.main()
