from diagrams.eraser import entity_relationship as diagram


def teardown_function():
    diagram.EntityRelationship.reset()


def test_entity_properties():
    node = diagram.Entity(name="node", icon="node-icon", color="node-color")

    assert node.properties.icon == "node-icon"
    assert node.properties.color == "node-color"

    content = node.render()

    assert "[icon: node-icon, color: node-color]" in content


def test_one_to_on_relationship(stdout):
    user = diagram.Entity(name="user")
    user_id = user.add_attribute("user_id")
    profile = diagram.Entity(name="profile")
    profile_id = profile.add_attribute("profile_id")

    user_id.one_to_one(profile_id)

    diagram.EntityRelationship.draw(stdout)

    assert "user.user_id - profile.profile_id" in stdout[-1]


def test_one_to_many_relationship(stdout):
    user = diagram.Entity(name="user")
    user_id = user.add_attribute("user_id")
    article = diagram.Entity(name="article")
    article_id = article.add_attribute("article_id")

    user_id.one_to_many(article_id)

    diagram.EntityRelationship.draw(stdout)

    assert "user.user_id < article.article_id" in stdout[-1]


def test_many_to_one_relationship(stdout):
    user = diagram.Entity(name="user")
    user_id = user.add_attribute("user_id")
    team = diagram.Entity(name="team")
    team_id = team.add_attribute("team_id")

    user_id.many_to_one(team_id)

    diagram.EntityRelationship.draw(stdout)

    assert "user.user_id > team.team_id" in stdout[-1]


def test_many_to_many_relationship(stdout):
    user = diagram.Entity(name="user")
    user_id = user.add_attribute("user_id")
    task = diagram.Entity(name="task")
    task_id = task.add_attribute("task_id")

    user_id.many_to_many(task_id)

    diagram.EntityRelationship.draw(stdout)

    assert "user.user_id <> task.task_id" in stdout[-1]
