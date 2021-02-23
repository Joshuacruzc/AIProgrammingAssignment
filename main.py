from aima.agents import *


class ExtendableVacuumEnvironment(Environment):

    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        locations = {}
        for x in range(width):
            for y in range(height):
                locations[(x, y)] = random.choice(['Clean', 'Dirty'])
        self.status = locations

    def thing_classes(self):
        return [Wall, Dirt, ReflexVacuumAgent, RandomVacuumAgent,
                TableDrivenVacuumAgent, ModelBasedVacuumAgent]

    def percept(self, agent):
        """Returns the agent's location, and the location status (Dirty/Clean)."""
        return agent.location, self.status[agent.location]

    def execute_action(self, agent, action):
        """Change agent's location and/or location's status; track performance.
        Score 10 for each dirt cleaned; -1 for each move."""
        if action == 'Right':
            if agent.location[0] != self.width - 1:
                agent.location = (agent.location[0] + 1, agent.location[1])
            agent.performance -= 1
        elif action == 'Left':
            if agent.location[0] != 0:
                agent.location = (agent.location[0] - 1, agent.location[1])
            agent.performance -= 1
        elif action == 'Up':
            if agent.location[1] != 0:
                agent.location = (agent.location[0], agent.location[1] - 1)
            agent.performance -= 1
        elif action == 'Down':
            if agent.location[1] != self.height - 1:
                agent.location = (agent.location[0], agent.location[1] + 1)
            agent.performance -= 1
        elif action == 'Suck':
            if self.status[agent.location] == 'Dirty':
                agent.performance += 10
            self.status[agent.location] = 'Clean'

    def default_location(self, thing):
        """Agents start in either location at random."""
        return random.choice(list(self.status.keys()))


def SimpleReflexAgentProgram():
    def program(percept):
        loc, status = percept
        return ('Suck' if status == 'Dirty'
                else 'Right' if loc == (0,0)
        else 'Left')

    return program


def ModelBasedVacuumAgent():
    """An agent that keeps track of what locations are clean or dirty.
    >>> agent = ModelBasedVacuumAgent()
    >>> environment = TrivialVacuumEnvironment()
    >>> environment.add_thing(agent)
    >>> environment.run()
    >>> environment.status == {(1,0):'Clean' , (0,0) : 'Clean'}
    True
    """
    model = {
        "last_location": None,
        "direction": ["Right", "Down", "Left", "Up"],
        "direction_index": 0
    }

    def program(percept):
        """Same as ReflexVacuumAgent, except if everything is clean, do NoOp."""
        location, status = percept
        model[location] = status  # Update the model here
        if all(model[location] == "Clean" for location in model.keys()):
            model['last_location'] = location
            return 'NoOp'
        elif status == 'Dirty':
            model['last_location'] = location
            return 'Suck'
        if location == model['last_location'] or location in model:
            model['direction_index'] = (model['direction_index'] + 1) % 4

    return Agent(program)


def simulate_agent_program_in_environment(env, agent, steps):
    env.add_thing(agent)
    print("Initial State of the Environment: {}.".format(env.status))
    for x in range(steps):
        env.step()
    print("Final State of the Environment: {}.".format(env.status))
    print("Agent Performance: " + str(agent.performance))


if __name__ == "__main__":
    # Answering 2.11 a-b
    random_agent_program = Agent(RandomAgentProgram(
        ['Right', 'Left', 'Down', 'Up', 'Suck', 'NoOp']))
    simple_reflex_agent = Agent(SimpleReflexAgentProgram())
    model_based_reflex_agent = ModelBasedVacuumAgent()
    print("---------------Simulating Simple Reflex Agent---------------------")
    simulate_agent_program_in_environment(ExtendableVacuumEnvironment(10, 10),
                                          simple_reflex_agent, 100)
    print("-------------------Simulating Random Agent------------------------")
    simulate_agent_program_in_environment(ExtendableVacuumEnvironment(10, 10),
                                          random_agent_program, 100)

    # Answering 2.11 c
    print("-------------------Simulating Random in extra small environment------------------------")
    simulate_agent_program_in_environment(ExtendableVacuumEnvironment(1, 1),
                                          random_agent_program, 100)

    # Answering 2.11 d
    print(
        "-------------------Simulating ModelBased Agent------------------------")
    simulate_agent_program_in_environment(ExtendableVacuumEnvironment(10, 10),
                                          model_based_reflex_agent, 100)