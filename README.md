# SimplePlanning - A planning tool in Python.

## Set up the project
Prerequisites: [virtualenv](http://virtualenv.readthedocs.org/en/latest/)
```
# Clone the repo
$ git clone https://github.com/GeorgeNagel/simpleplanning.git
$ cd simpleplanning
# Create a virtualenv
$ virtualenv venv
# Activate the virtualenv
$ source venv/bin/activate
```
## Run the tests
```
# Run the tests
(venv)$ sh test.sh
.................................
----------------------------------------------------------------------
Ran 33 tests in 0.267s

OK
```
## Run the demo
```
(venv)$ sh fake_game.sh

Arthur's goal: <has sword, [<Guinevere>]: True>
Guinevere's goal: <is alive, [<Guinevere>]: False>
Lancelot's goal: <has sword, [<Arthur>]: True>
Arthur's turn.
Arthur performs steal sword on {'victim': <Lancelot>}
Lancelot's goal is satisfied.
```
## To do
1. Probabilistic actions (currently actions are assumed to have 100% success rate.)
2. Goal evaluation (goals are currently selected at random)
3. Hooks for emotional evaluation of plans