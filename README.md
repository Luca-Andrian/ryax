# Default Ryax Actions and Triggers

These are default Actions and Triggers that come pre-built on Ryax instances.
All of these Actions and Triggers are available in an MPL2 license, feel free to use these Actions and Triggers to make your own!


## Contents

- [Triggers](triggers)
- [Actions](actions)
- [Tests](tests/)

## Requirements

* Python 3.7+ ([Installation Guide](https://wiki.python.org/moin/BeginnersGuide/))
* Poetry ([Installation Guide](https://python-poetry.org/docs/#installation))

## Conventions

- **Unit Tests**: Unit test each action separately in its own file under the proper subdirectory located in `tests/`. This also eliminates the need to add test cases in the handler file itself under an `if __name__=='__main__'` statement. 
- **Print Statements**: limit print statements to a minimum. They are helpful in some cases, for example when the action connects to an external service it could be good to document the progress of that interaction, or in the case where a action uses some small, intermediate data that is interesting to print in a few lines (such as a list of files that were zipped together).
- **Type Annotations**: use type annotations in function signatures as much as possible. Once the python runtime in ryax surpasses 3.7, use `TypedDict` to type annotate the inputs and/or outputs of an action in the python code (even though it is also defined in the `ryax_metadata.yaml`)

## How testing is done?

Tests are started with the `test.sh` script.
It wraps a `pytest` command.
In this repository there is only unit tests.
We use some `pytest` tricks to mock the environment of each action.
With this method we can test actions without requiring setting external services like a database or access to a SaaS product.

## Merging new actions

The process is entirely automatic and is made each time a branch is merged into
master. Once built, they will be available in any newly created SaaS instance.
Make sure your actions are tested before merging!
