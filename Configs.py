class Lexer:
    def __init__(self):
        with open("_internal/A-90-CONFIGURATION.cfg", 'r', encoding="utf-8") as cfgFile:
            self.ConfigurationText=cfgFile.read()
        if self.ConfigurationText == "": raise BaseException("Cannot import the configuration: Configuration is not alright.")
        self.configs=[]
        pos=0
        remain = self.ConfigurationText
        for symbol in self.ConfigurationText:
            pos+=1
            if symbol == ';':
                popIndex=0
                if not self.configs: popIndex=pos
                self.configs.append(remain[pos-popIndex:])
                remain = remain[:pos]
        for config in self.configs:
            print(config)
configsLexer = Lexer()
