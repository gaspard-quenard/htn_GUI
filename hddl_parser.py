from unified_planning.io import PDDLReader
from data_structures.param import Param




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

    methods_which_can_do_this_task = []
    # Get all the methods which can resolve this task
    for method in hddl_problem.methods:
        if method.achieved_task.task == initial_task.task:
            methods_which_can_do_this_task.append(method)


    print(f"{initial_task} can be resolved by the following methods: {[method.name for method in methods_which_can_do_this_task]}")
    return task_network.subtasks



if __name__ == '__main__':
    domain_path = "/home/gaspard/LIG/Code/htn_GUI/hddl/domain.hddl"
    problem_path = "/home/gaspard/LIG/Code/htn_GUI/hddl/p00.hddl"
    parse_hddl(domain_file=domain_path, problem_file=problem_path)