from ecospy import EcosSimulation, EcosSimulationStructure
from ecospy.plotter import Plotter, TimeSeriesConfig
import numpy as np

if __name__ == '__main__':
    ss = EcosSimulationStructure()
    ss.add_model("cart", "fmus/Cart.fmu")
    ss.add_model("pendulum", "fmus/Pendulum.fmu")
    ss.add_model("controller", "fmus/Controller.fmu")

    # Koble modellane saman
    ss.make_real_connection("controller::force", "cart::force")
    ss.make_real_connection("cart::acceleration", "pendulum::cart_acceleration")
    ss.make_real_connection("cart::position", "controller::cart_position")
    ss.make_real_connection("cart::velocity", "controller::cart_velocity")
    ss.make_real_connection("pendulum::angle", "controller::angle")
    ss.make_real_connection("pendulum::angular_velocity", "controller::angular_velocity")
    ss.make_real_connection("pendulum::force", "cart::force_pendulum")

    # Legg til initialverdiar
    params = {
    # Pendulum
    "pendulum::length_pendulum": 1.0,      # meter
    "pendulum::mass_pendulum": 0.1,        # kg
    "pendulum::angle": 20 * np.pi / 180,   # startvinkel (20 grader)
    "pendulum::angular_velocity": 0.0,     # start vinkelhastighet

    # Cart
    "cart::mass_cart": 1.0,                 # vognmasse
    "cart::mass_pendulum": 0.1,             # pendelmasse
    "cart::position": 0.0,                  # start posisjon
    "cart::velocity": 0.0                   # start hastigheit
    }

    ss.add_parameter_set("initialValues", params)

    result_file = "results.csv"

    with EcosSimulation(structure=ss, step_size=0.01) as sim:
        sim.add_csv_writer(result_file)
        sim.init(parameter_set="initialValues")
        sim.step_until(100)
        sim.terminate()

    # Plotting
    config = TimeSeriesConfig(
        title="Cart-Pendulum System",
        y_label="Value",
        identifiers=[
            "pendulum::angle",
            "cart::position"
        ]
    )

    plotter = Plotter(result_file, config)
    plotter.show()