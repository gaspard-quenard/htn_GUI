from unified_planning.io import PDDLReader





def parse_hddl(domain_file: str, problem_file: str):
    reader = PDDLReader()
    try:
        hddl_problem = reader.parse_problem(domain_file, problem_file)
    except:
        print("Error while parsing HDDL domain and problem")
        return None
    
    task_network = hddl_problem.task_network

    # TODO: first, create an action with the initial state as effect (and no precondition)
    # This action will be the root of the tree


    # Get all methods which can accomplish the task
    initial_task = task_network.subtasks[0]

    # methods = 
    return task_network.subtasks