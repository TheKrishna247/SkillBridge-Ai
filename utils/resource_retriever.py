from learning_resources import LEARNING_RESOURCES

def get_resources(skill):
    skill = skill.lower().strip()

    for key in LEARNING_RESOURCES:
        if key in skill:
            return LEARNING_RESOURCES[key]

    return None
