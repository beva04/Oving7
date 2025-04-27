from pythonfmu import Fmi2Slave, Real, Fmi2Causality
import numpy as np

class Pendulum(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.length_pendulum = 1.0  # meter
        self.mass_pendulum = 0.1    # kg
        self.gravity = 9.81  # m/s²

        self.angle = 0.349  # rad
        self.angular_velocity = 0.0
        self.cart_acceleration = 0.0
        self.force = 0.0

        self.register_variable(Real("length_pendulum", causality=Fmi2Causality.parameter))
        self.register_variable(Real("mass_pendulum", causality=Fmi2Causality.parameter))
        self.register_variable(Real("angle", causality=Fmi2Causality.output))
        self.register_variable(Real("angular_velocity", causality=Fmi2Causality.output))
        self.register_variable(Real("force", causality=Fmi2Causality.output))
        self.register_variable(Real("cart_acceleration", causality=Fmi2Causality.input))

    def do_step(self, t, dt):
        T_gravity = self.mass_pendulum * self.gravity * self.length_pendulum * np.sin(self.angle)

        theta_ddot = (T_gravity - (self.mass_pendulum * self.length_pendulum * np.cos(self.angle) * self.cart_acceleration)) / (self.mass_pendulum * self.length_pendulum**2)

        self.angular_velocity += theta_ddot * dt
        self.angle += self.angular_velocity * dt

        self.force = self.mass_pendulum * self.length_pendulum * (np.sin(self.angle) * self.angular_velocity**2 - np.cos(self.angle) * theta_ddot)