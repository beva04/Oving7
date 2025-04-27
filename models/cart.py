from pythonfmu import Fmi2Slave, Real, Fmi2Causality
import numpy as np

class Cart(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mass_cart = 1.0  # kg
        self.position = 0.0
        self.velocity = 0.0
        self.acceleration = 0.0
        self.force = 0.0

        self.mass_pendulum = 0.0
        self.force_pendulum = 0.0

        self.register_variable(Real("mass_cart", causality=Fmi2Causality.parameter))
        self.register_variable(Real("mass_pendulum", causality=Fmi2Causality.parameter))
        self.register_variable(Real("position", causality=Fmi2Causality.output))
        self.register_variable(Real("velocity", causality=Fmi2Causality.output))
        self.register_variable(Real("acceleration", causality=Fmi2Causality.output))
        self.register_variable(Real("force", causality=Fmi2Causality.input))
        self.register_variable(Real("force_pendulum", causality=Fmi2Causality.input))

    def do_step(self, t, dt):
        self.acceleration = (self.force + self.force_pendulum) / (self.mass_cart + self.mass_pendulum)
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt