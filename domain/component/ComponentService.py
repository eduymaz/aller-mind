from domain.component.ComponentRepository import ComponentRepository

def create_component(component_entity):
    component_repository = ComponentRepository()
    try:
        component_repository.create(component_entity)
        print("ComponentEntity instance saved successfully.")
    except Exception as e:
        print(f"Error saving ComponentEntity instance: {e}")

def fetch_all_components():
    component_repository = ComponentRepository()
    try:
        components = component_repository.select_all()
        print("All components fetched from the database:")
        for component in components:
            print(component)
    except Exception as e:
        print(f"Error fetching components: {e}")

