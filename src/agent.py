import json

class Agent:
    def __init__(self, name, sys_prompt=None, workflow=None):
        self.name = name
        self.messages = [{"role": "system", "content": sys_prompt}]
        self.workflow = workflow

    def handle_turn(self, user_input):
        self.messages.append({"role": "user", "content": user_input})
        reply = self.workflow.run(self.messages)
        return reply
        
    def run(self):
        print(f"{self.name} 启动成功！请输入您的问题（输入 'exit' 退出）：")
        while True:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                print("退出程序。")
                break
            response = self.handle_turn(user_input)
            print(f"{self.name}: {response}")
            

            

            

            

