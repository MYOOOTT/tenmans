import unittest
from lobby import Lobby

class LobbyTest(unittest.TestCase):
    def setUp(self):
        self.lobby = Lobby(4)

    def test_add(self):
        self.lobby.add("Player") 
        self.assertIn("Player", self.lobby.player_list)
    
    def test_multiple_add(self):
        self.lobby.add("Player1", "Player2")
        self.assertTrue("Player1" in self.lobby.player_list and "Player2" in self.lobby.player_list, msg=str(self.lobby.player_list))
    
    def test_duplicate_add(self):
        self.lobby.add("Player") 
        self.assertRaises(AssertionError, self.lobby.add, "Player")

    def test_lobby_max(self):
        self.lobby.add("1")
        self.lobby.add("2")
        self.lobby.add("3")
        self.lobby.add("4")
        self.assertRaises(AssertionError, self.lobby.add, "5")

    def test_remove(self):
        self.lobby.add("Player")
        self.lobby.remove("Player")
        self.assertNotIn("Player", self.lobby.player_list)

    def test_remove_nonexisting(self):
        self.assertRaises(ValueError, self.lobby.remove, "Player")

    def test_shuffle(self):
        self.lobby.add("1", "2", "3", "4")
        self.lobby.shuffle()
        self.assertTrue(self.lobby.get_team_one and self.lobby.get_team_two)

    def test_swap(self):
        self.lobby.add("Player1", "Player2")
        self.lobby.team_one.add("Player1")
        self.lobby.team_two.add("Player2")
        self.lobby.swap("Player1", "Player2")
        self.assertTrue("Player1" in self.lobby.team_two and "Player2" in self.lobby.team_one)

    def test_spots_left(self):
        self.lobby.add("Player1", "Player2")
        self.assertEqual(self.lobby.spots_left(), 2)

if __name__ == '__main__':
    unittest.main()