
class CataLog():
    def __init__(self):
        self.HEADER  = '\033[1;94m'
        self.END     = '\033[0m'
        self.WARNING = '\033[1;95m'
        self.INFO    = '\033[1;92m'
        self.FAIL    = '\033[1;91m'

    def header(self, s:str):
        print(f"{self.HEADER} {s} {self.END}")
    
    def warning(self, s:str):
        print(f"{self.WARNING} {s} {self.END}")

    def info(self, s:str,end='\n'):
        print(f"{self.INFO} {s} {self.END}",end=end)
    
    def fail(self, s:str):
        print(f"{self.FAIL} {s} {self.END}")