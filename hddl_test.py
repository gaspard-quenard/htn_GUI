from unified_planning.io import PDDLReader


if __name__ == "__main__":

    # We use PDDL reader to read HDDL files as well
    reader = PDDLReader()
    hddl_problem = reader.parse_problem("/home/gaspard/LIG/Code/macro_actions/benchmarks/ipc2020/total-order/Blocksworld-GTOHP/domain.hddl", "/home/gaspard/LIG/Code/macro_actions/benchmarks/ipc2020/total-order/Blocksworld-GTOHP/p01.hddl")

    # Feel free to explore the hddl_problem object
    #...
    #


    task_network = hddl_problem.task_network
    print(task_network)

    subtasks = task_network.subtasks