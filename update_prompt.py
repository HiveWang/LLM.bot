
class UpdateSystemMessage:
    def __init__(self,system_message):
        self.system_message = system_message

    def update_system_message(self, **kwargs):
        try:
            # print(f"Update system messsage {kwargs}")#debug
            self.system_message = self.system_message.format(**kwargs,)
        except KeyError as e:
            print("KeyError occurred:",e)

    def _str__(self):
        return self.system_message
