def myAverage(a, b, c, d):
    return str(round((a + b + c + d) / 4,3))

def whichGreater(ergo, beta):
    if(ergo > beta):
        return "ergo is greater"
    else:
        return "beta is greater"

def takeSquareRoot(pan, myMessage="The square root of the number is: "):
    return myMessage + str(pan ** 0.5)

tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "myAverage",
                        "description": "Calculates the average of four numbers, then rounds the result to three decimal places",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "a": {
                                    "type": "number",
                                    "description": "first number to be averaged",
                                },
                                "b": {
                                    "type": "number",
                                    "description": "second number to be averaged",
                                },
                                "c": {
                                    "type": "number",
                                    "description": "third number to be averaged",
                                },
                                "d": {
                                    "type": "number",
                                    "description": "forth number to be averaged",
                                }
                            },
                            "required": ["a","b","c","d"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "takeSquareRoot",
                        "description": "Recieves a number or a number and a message and returns the square root of the number or the message concatenated with the square root of the number",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "pan": {
                                    "type": "number",
                                    "description": "a number to be compared",
                                },
                                "myMessage": {
                                    "type": "string",
                                    "description": "a message to indicate the result of the comparison",
                                }
                            },
                            "required": ["pan"],
                        },
                    },
                }
        ]
