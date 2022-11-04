class RyaxGateway:
    def __init__(self, inputs_values: dict = {}):
        self.inputs_values = {k: v for k, v in inputs_values.items()}

    async def send_execution(self, outputs_values: dict):
        return outputs_values


def main(GatewayClass: RyaxGateway):
    pass
