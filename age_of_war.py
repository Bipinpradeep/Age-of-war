from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Tuple, Optional
from itertools import permutations


class UnitType(Enum):
    """Enumeration of all soldier unit types"""
    MILITIA = "Militia"
    SPEARMEN = "Spearmen"
    LIGHT_CAVALRY = "LightCavalry"
    HEAVY_CAVALRY = "HeavyCavalry"
    FOOT_ARCHER = "FootArcher"
    CAVALRY_ARCHER = "CavalryArcher"


class BattleOutcome(Enum):
    """Enumeration of possible battle outcomes"""
    WIN = "Win"
    DRAW = "Draw"
    LOSS = "Loss"


class Unit(ABC):
    """Abstract base class for all military units"""
    
    def __init__(self, count: int):
        self._count = count
        self._unit_type = self._get_unit_type()
    
    @property
    def count(self) -> int:
        return self._count
    
    @property
    def unit_type(self) -> UnitType:
        return self._unit_type
    
    @abstractmethod
    def _get_unit_type(self) -> UnitType:
        """Return the specific unit type"""
        pass
    
    @abstractmethod
    def get_advantages(self) -> List[UnitType]:
        """Return list of unit types this unit has advantage over"""
        pass
    
    def has_advantage_over(self, other_unit: 'Unit') -> bool:
        """Check if this unit has advantage over another unit"""
        return other_unit.unit_type in self.get_advantages()
    
    def __str__(self) -> str:
        return f"{self.unit_type.value}#{self.count}"


class Militia(Unit):
    def _get_unit_type(self) -> UnitType:
        return UnitType.MILITIA
    
    def get_advantages(self) -> List[UnitType]:
        return [UnitType.SPEARMEN, UnitType.LIGHT_CAVALRY]


class Spearmen(Unit):
    def _get_unit_type(self) -> UnitType:
        return UnitType.SPEARMEN
    
    def get_advantages(self) -> List[UnitType]:
        return [UnitType.LIGHT_CAVALRY, UnitType.HEAVY_CAVALRY]


class LightCavalry(Unit):
    def _get_unit_type(self) -> UnitType:
        return UnitType.LIGHT_CAVALRY
    
    def get_advantages(self) -> List[UnitType]:
        return [UnitType.FOOT_ARCHER, UnitType.CAVALRY_ARCHER]


class HeavyCavalry(Unit):
    def _get_unit_type(self) -> UnitType:
        return UnitType.HEAVY_CAVALRY
    
    def get_advantages(self) -> List[UnitType]:
        return [UnitType.MILITIA, UnitType.FOOT_ARCHER, UnitType.LIGHT_CAVALRY]


class FootArcher(Unit):
    def _get_unit_type(self) -> UnitType:
        return UnitType.FOOT_ARCHER
    
    def get_advantages(self) -> List[UnitType]:
        return [UnitType.MILITIA, UnitType.CAVALRY_ARCHER]


class CavalryArcher(Unit):
    def _get_unit_type(self) -> UnitType:
        return UnitType.CAVALRY_ARCHER
    
    def get_advantages(self) -> List[UnitType]:
        return [UnitType.SPEARMEN, UnitType.HEAVY_CAVALRY]


class UnitFactory:
    """Factory class for creating unit instances"""
    
    _unit_classes = {
        UnitType.MILITIA: Militia,
        UnitType.SPEARMEN: Spearmen,
        UnitType.LIGHT_CAVALRY: LightCavalry,
        UnitType.HEAVY_CAVALRY: HeavyCavalry,
        UnitType.FOOT_ARCHER: FootArcher,
        UnitType.CAVALRY_ARCHER: CavalryArcher
    }
    
    @classmethod
    def create_unit(cls, unit_type: UnitType, count: int) -> Unit:
        """Create a unit instance based on type and count"""
        unit_class = cls._unit_classes.get(unit_type)
        if not unit_class:
            raise ValueError(f"Unknown unit type: {unit_type}")
        return unit_class(count)


class Battle:
    """Represents a single battle between two units"""
    
    ADVANTAGE_MULTIPLIER = 2
    
    def __init__(self, attacker: Unit, defender: Unit):
        self._attacker = attacker
        self._defender = defender
        self._outcome = self._calculate_outcome()
    
    @property
    def attacker(self) -> Unit:
        return self._attacker
    
    @property
    def defender(self) -> Unit:
        return self._defender
    
    @property
    def outcome(self) -> BattleOutcome:
        return self._outcome
    
    def _calculate_outcome(self) -> BattleOutcome:
        """Calculate the outcome of this battle"""
        effective_attacker_count = self._get_effective_count()
        defender_count = self._defender.count
        
        if effective_attacker_count > defender_count:
            return BattleOutcome.WIN
        elif effective_attacker_count == defender_count:
            return BattleOutcome.DRAW
        else:
            return BattleOutcome.LOSS
    
    def _get_effective_count(self) -> int:
        """Calculate effective count considering advantages"""
        if self._attacker.has_advantage_over(self._defender):
            return self._attacker.count * self.ADVANTAGE_MULTIPLIER
        elif self._defender.has_advantage_over(self._attacker):
            return self._attacker.count // self.ADVANTAGE_MULTIPLIER
        else:
            return self._attacker.count
    
    def __str__(self) -> str:
        return f"{self._attacker} vs {self._defender} -> {self._outcome.value}"


class Army:
    """Represents an army consisting of multiple platoons"""
    
    def __init__(self, platoons: List[Unit]):
        self._platoons = platoons
    
    @property
    def platoons(self) -> List[Unit]:
        return self._platoons.copy()
    
    def get_platoon_count(self) -> int:
        return len(self._platoons)
    
    def __str__(self) -> str:
        return ';'.join(str(platoon) for platoon in self._platoons)


class PlatoonParser:
    """Parser for converting string input to Army objects"""
    
    @staticmethod
    def parse_army(platoon_string: str) -> Army:
        """Parse platoon string into Army object"""
        platoons = []
        for platoon_data in platoon_string.split(';'):
            unit_type_str, count_str = platoon_data.split('#')
            unit_type = UnitType(unit_type_str)
            count = int(count_str)
            unit = UnitFactory.create_unit(unit_type, count)
            platoons.append(unit)
        return Army(platoons)


class WarSimulation:
    """Simulates a war with multiple battles"""
    
    REQUIRED_WINS = 3
    
    def __init__(self, attacking_army: Army, defending_army: Army):
        self._attacking_army = attacking_army
        self._defending_army = defending_army
        self._validate_armies()
    
    def _validate_armies(self):
        """Validate that both armies have the same number of platoons"""
        if (self._attacking_army.get_platoon_count() != 
            self._defending_army.get_platoon_count()):
            raise ValueError("Armies must have the same number of platoons")
    
    def find_winning_arrangement(self) -> Optional[Army]:
        """Find an arrangement of attacking army that wins the war"""
        defending_platoons = self._defending_army.platoons
        
        for arrangement in permutations(self._attacking_army.platoons):
            battles = self._simulate_battles(list(arrangement), defending_platoons)
            if self._is_winning_arrangement(battles):
                return Army(list(arrangement))
        
        return None
    
    def _simulate_battles(self, attacking_platoons: List[Unit], 
                         defending_platoons: List[Unit]) -> List[Battle]:
        """Simulate battles between corresponding platoons"""
        battles = []
        for attacker, defender in zip(attacking_platoons, defending_platoons):
            battle = Battle(attacker, defender)
            battles.append(battle)
        return battles
    
    def _is_winning_arrangement(self, battles: List[Battle]) -> bool:
        """Check if the arrangement results in victory"""
        wins = sum(1 for battle in battles if battle.outcome == BattleOutcome.WIN)
        return wins >= self.REQUIRED_WINS
    
    def get_battle_report(self, army_arrangement: Army) -> List[Battle]:
        """Get detailed battle report for a specific arrangement"""
        return self._simulate_battles(army_arrangement.platoons, 
                                    self._defending_army.platoons)


class BattleReporter:
    """Handles reporting of battle results"""
    
    @staticmethod
    def print_detailed_report(arrangement: Army, battles: List[Battle]):
        """Print detailed battle report"""
        print("Winning arrangement found:")
        print(arrangement)
        print("\nBattle details:")
        
        wins = 0
        for i, battle in enumerate(battles, 1):
            print(f"Battle {i}: {battle}")
            if battle.outcome == BattleOutcome.WIN:
                wins += 1
        
        print(f"\nResult: {wins}/{len(battles)} battles won")
    
    @staticmethod
    def print_no_solution():
        """Print message when no winning arrangement exists"""
        print("There is no chance of winning")


class AgeOfWarGame:
    """Main game controller class"""
    
    def __init__(self):
        self._parser = PlatoonParser()
        self._reporter = BattleReporter()
    
    def solve_war_scenario(self, attacking_army_str: str, defending_army_str: str) -> str:
        """Solve the war scenario and return the result"""
        try:
            attacking_army = self._parser.parse_army(attacking_army_str)
            defending_army = self._parser.parse_army(defending_army_str)
            
            simulation = WarSimulation(attacking_army, defending_army)
            winning_arrangement = simulation.find_winning_arrangement()
            
            if winning_arrangement:
                battles = simulation.get_battle_report(winning_arrangement)
                self._reporter.print_detailed_report(winning_arrangement, battles)
                return str(winning_arrangement)
            else:
                self._reporter.print_no_solution()
                return "There is no chance of winning"
                
        except Exception as e:
            error_msg = f"Error processing input: {str(e)}"
            print(error_msg)
            return error_msg


class GameTestSuite:
    """Test suite for the game"""
    
    def __init__(self):
        self._game = AgeOfWarGame()
    
    def run_sample_test(self):
        """Run the provided sample test case"""
        print("=" * 60)
        print("SAMPLE TEST CASE")
        print("=" * 60)
        
        attacking_army = "Spearmen#10;Militia#30;FootArcher#20;LightCavalry#1000;HeavyCavalry#120"
        defending_army = "Militia#10;Spearmen#10;FootArcher#1000;LightCavalry#120;CavalryArcher#100"
        
        print(f"Attacking army: {attacking_army}")
        print(f"Defending army: {defending_army}")
        print()
        
        result = self._game.solve_war_scenario(attacking_army, defending_army)
        print(f"\nFinal Answer: {result}")
    
    def run_custom_test(self):
        """Run a custom test case with user input"""
        print("\n" + "=" * 60)
        print("CUSTOM TEST CASE")
        print("=" * 60)
        
        attacking_army = input("Enter your army (format: Class#Count;Class#Count;...): ")
        defending_army = input("Enter opponent army (format: Class#Count;Class#Count;...): ")
        
        result = self._game.solve_war_scenario(attacking_army, defending_army)
        print(f"\nResult: {result}")
    
    def run_unit_tests(self):
        """Run basic unit tests"""
        print("\n" + "=" * 60)
        print("UNIT TESTS")
        print("=" * 60)
        
        # Test unit creation
        militia = UnitFactory.create_unit(UnitType.MILITIA, 30)
        spearmen = UnitFactory.create_unit(UnitType.SPEARMEN, 10)
        
        # Test advantage system
        assert militia.has_advantage_over(spearmen), "Militia should have advantage over Spearmen"
        assert not spearmen.has_advantage_over(militia), "Spearmen should not have advantage over Militia"
        
        # Test battle outcome
        battle = Battle(militia, spearmen)
        assert battle.outcome == BattleOutcome.WIN, "Militia should win against Spearmen"
        
        print("✓ All unit tests passed!")


def main():
    """Main console application entry point"""
    print("AGE OF WAR - Battle Strategy Solver")
    print("=" * 40)
    
    test_suite = GameTestSuite()
    
    # Run sample test
    test_suite.run_sample_test()
    
    # Run unit tests
    test_suite.run_unit_tests()
    
    # Offer custom test
    while True:
        choice = input("\nRun custom test? (y/n): ").lower().strip()
        if choice == 'y':
            test_suite.run_custom_test()
        elif choice == 'n':
            break
        else:
            print("Please enter 'y' or 'n'")
    
    print("\nThank you for using Age of War Battle Strategy Solver!")


if __name__ == "__main__":
    main()
