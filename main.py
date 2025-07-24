from view import Main
from controller import Controller
from model import Model

if __name__ == "__main__":
    model = Model()
    controller = Controller(model)  
    Main(controller).iniciar()      
