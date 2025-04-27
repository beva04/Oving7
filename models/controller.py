from pythonfmu import Fmi2Slave, Real, Fmi2Causality

class Controller(Fmi2Slave):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Regulatorparametre
        self.k1 = 1.0
        self.k2 = 2.0
        self.k3 = 30.0
        self.k4 = 10.0

        self.angle = 0.0
        self.angular_velocity = 0.0
        self.cart_position = 0.0
        self.cart_velocity = 0.0
        self.force = 0.0

        # Registrer variablane
        self.register_variable(Real("angle", causality=Fmi2Causality.input))
        self.register_variable(Real("angular_velocity", causality=Fmi2Causality.input))
        self.register_variable(Real("cart_position", causality=Fmi2Causality.input))
        self.register_variable(Real("cart_velocity", causality=Fmi2Causality.input))
        self.register_variable(Real("force", causality=Fmi2Causality.output))

    def do_step(self, t, dt):
        self.force = (- (self.k1 * self.angle) - (self.k2 * self.angular_velocity) - (self.k3 * self.cart_position) - (self.k4 * self.cart_velocity))