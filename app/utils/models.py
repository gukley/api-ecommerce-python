import pkgutil
import importlib
import os


def load_models():
    models_path = os.path.join(os.path.dirname(__file__), "../models")
    module_prefix = "app.models"
    for _, module_name, _ in pkgutil.iter_modules([models_path]):
        importlib.import_module(f"{module_prefix}.{module_name}")
