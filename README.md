# Age of War - Battle Strategy Solver

A comprehensive object-oriented Python solution for solving medieval battle strategy problems. This application helps determine the optimal arrangement of military platoons to achieve victory in simultaneous battles.

## 📋 Problem Description

You are a medieval king attacking your opponent at five locations simultaneously. Each location has a platoon with soldiers of a specific class. Your goal is to arrange your platoons to win the majority of battles (at least 3 out of 5).

### Battle Mechanics

- **Basic Rule**: One soldier can handle one enemy soldier
- **Advantage System**: Units with class advantage can handle 2x enemy soldiers
- **Victory Conditions**: Win majority of battles (≥3/5)

### Unit Classes & Advantages

| Unit Class | Advantages Over |
|------------|----------------|
| Militia | Spearmen, Light Cavalry |
| Spearmen | Light Cavalry, Heavy Cavalry |
| Light Cavalry | Foot Archer, Cavalry Archer |
| Heavy Cavalry | Militia, Foot Archer, Light Cavalry |
| Cavalry Archer | Spearmen, Heavy Cavalry |
| Foot Archer | Militia, Cavalry Archer |

## 🏗️ Architecture & Design

### Object-Oriented Design Principles

- **Abstraction**: Abstract `Unit` base class with common interface
- **Encapsulation**: Private attributes with controlled access via properties
- **Inheritance**: All unit types inherit from `Unit` base class
- **Polymorphism**: Uniform treatment of different unit types
- **Composition**: Complex objects built from simpler components

### Design Patterns Implemented

- **Factory Pattern**: `UnitFactory` for creating unit instances
- **Strategy Pattern**: Each unit encapsulates its own advantage rules
- **Single Responsibility**: Each class has one clear purpose

### Key Classes

```
Unit (Abstract)
├── Militia
├── Spearmen
├── LightCavalry
├── HeavyCavalry
├── FootArcher
└── CavalryArcher

Core Components:
- Army: Collection of units
- Battle: Single combat simulation
- WarSimulation: Multi-battle orchestration
- AgeOfWarGame: Main game controller
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- No external dependencies required (uses only standard library)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/age-of-war.git
cd age-of-war
```

2. Run the application:
```bash
python age_of_war.py
```

### Input Format

```
Class#Count;Class#Count;Class#Count;Class#Count;Class#Count
```

**Example:**
```
Spearmen#10;Militia#30;FootArcher#20;LightCavalry#1000;HeavyCavalry#120
```

## 💻 Usage

### Running the Application

```bash
python age_of_war.py
```

The application will:
1. Run the sample test case automatically
2. Execute unit tests
3. Offer option for custom input testing

### Sample Input/Output

**Input:**
```
Your army: Spearmen#10;Militia#30;FootArcher#20;LightCavalry#1000;HeavyCavalry#120
Enemy army: Militia#10;Spearmen#10;FootArcher#1000;LightCavalry#120;CavalryArcher#100
```

**Output:**
```
Winning arrangement found:
Militia#30;FootArcher#20;Spearmen#10;LightCavalry#1000;HeavyCavalry#120

Battle details:
Battle 1: Militia#30 vs Militia#10 -> Win
Battle 2: FootArcher#20 vs Spearmen#10 -> Win
Battle 3: Spearmen#10 vs FootArcher#1000 -> Loss
Battle 4: LightCavalry#1000 vs LightCavalry#120 -> Win
Battle 5: HeavyCavalry#120 vs CavalryArcher#100 -> Loss

Result: 3/5 battles won
```

## 🧪 Testing

### Built-in Test Suite

The application includes comprehensive testing:

- **Sample Test**: Validates the provided example
- **Unit Tests**: Tests individual components
- **Custom Tests**: Interactive testing with user input

### Running Tests

Tests run automatically when starting the application, or you can run specific test methods:

```python
from age_of_war import GameTestSuite

test_suite = GameTestSuite()
test_suite.run_unit_tests()
test_suite.run_sample_test()
```

## 📚 API Reference

### Core Classes

#### `Unit` (Abstract Base Class)
- `count`: Number of soldiers
- `unit_type`: Type of unit (enum)
- `has_advantage_over(other_unit)`: Check advantage
- `get_advantages()`: List of advantageous unit types

#### `Army`
- `platoons`: List of unit platoons
- `get_platoon_count()`: Number of platoons

#### `Battle`
- `attacker`: Attacking unit
- `defender`: Defending unit
- `outcome`: Battle result (Win/Draw/Loss)

#### `WarSimulation`
- `find_winning_arrangement()`: Find optimal arrangement
- `get_battle_report()`: Detailed battle analysis

#### `AgeOfWarGame`
- `solve_war_scenario(attacking_army_str, defending_army_str)`: Main solver

## 🔧 Configuration

### Customization Options

- **Required Wins**: Modify `REQUIRED_WINS` in `WarSimulation`
- **Advantage Multiplier**: Adjust `ADVANTAGE_MULTIPLIER` in `Battle`
- **New Unit Types**: Extend `Unit` class and update `UnitFactory`

### Adding New Unit Types

1. Create new class inheriting from `Unit`
2. Implement `_get_unit_type()` and `get_advantages()`
3. Add to `UnitType` enum
4. Update `UnitFactory._unit_classes`

```python
class NewUnit(Unit):
    def _get_unit_type(self) -> UnitType:
        return UnitType.NEW_UNIT
    
    def get_advantages(self) -> List[UnitType]:
        return [UnitType.TARGET_UNIT]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style Guidelines

- Follow PEP 8 conventions
- Use meaningful variable/function names
- Add docstrings for all public methods
- Maintain single responsibility principle
- Write tests for new features

## 📈 Performance

- **Time Complexity**: O(n!) where n is number of platoons (due to permutations)
- **Space Complexity**: O(n) for storing arrangements and battle results
- **Optimization**: Early termination when winning arrangement found

## 🐛 Known Issues

- Large armies (>7 platoons) may have performance issues due to factorial complexity
- Input validation could be more robust for edge cases

## 👥 Authors

- **Bipin Pradeep** - *Initial work* - [https://github.com/Bipinpradeep](https://github.com/yourusername)

## 🙏 Acknowledgments

- Medieval warfare strategy inspiration
- Object-oriented design principles
- Python community for best practices

## 📞 Support

For support, please open an issue on GitHub or contact [bipinpradeep00@gmail.com](mailto:bipinpradeep00@gmil.com).

---
