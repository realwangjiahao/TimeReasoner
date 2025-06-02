from openai import OpenAI
import torch.nn as nn


class deepseek_api_output(nn.Module):
    def __init__(self,api_key='',temperature=0.6,top_p=0.7):
        super(deepseek_api_output, self).__init__()
        self.client = OpenAI(base_url="https://api.deepseek.com",api_key=api_key)\
        self.temperature = temperature
        self.top_p = top_p
    
    def forward(self, content):
        response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": content},],stream=False,
                temperature=self.temperature,
                top_p=self.top_p,
                max_tokens=4096,)
        reasoning=response.choices[0].message.model_extra['reasoning_content']
        answer=response.choices[0].message.content        
        return reasoning,answer
    

