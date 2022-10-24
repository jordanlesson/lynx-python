import threading
from typing import Tuple, Dict
from eth_typing import Address
from lynx.consensus.epoch_context import EpochContext
from lynx.consensus.vrf import VRF
from eth_account import Account
from eth_typing import BlockNumber


class Leader:

    def __init__(self, address: Address, stake: int, campaign: int) -> None:
        """
        Initializes a Leader object representing a block leader. A block leader
        is a randomly chosen node responsible for proposing blocks in a particular
        time slot.
        """

        self.address = address
        self.stake = stake
        self.campaign = campaign


class LeaderSchedule:

    def __init__(self) -> None:
        """
        Initializes a leader schedule as a mapping of a block number
        to a Leader object.
        """

        self.leader_schedule : Dict[BlockNumber, Leader] = {}
        # self.leader_lock = threading.Lock()

    
    def __str__(self) -> str:
        """
        Returns the leader schedule mapping as a readable string.
        """

        return self.leader_schedule.__str__()


    @classmethod
    def generate_campaign(cls, epoch: EpochContext, account: Account) -> tuple:
        """Generates ten 256-bit random numbers to attempt to be
        elected as block leader for one of the slots in the current epoch."""

        rand_nums = []
        for block_number in range(epoch.start, epoch.end, epoch.slot_size):
            rand_num: Tuple[int, int] = VRF.generate_random_number(block_number=block_number, stake=69, account=account)
            rand_nums.append(rand_num)
            print(f'Random Number Generated for Block {block_number}: {str(rand_num)[:10]}...')

        return rand_nums

    
    def add_leader(self, block_number: BlockNumber, leader: Leader) -> None:
        """
        Adds a leader to the current leader schedule given the block number
        a validator campaigns for. Raises a ValueError if the potential leader's
        campaign is not greater than the current leader's campaign.
        """

        # self.leader_lock.acquire()
        if block_number in self.leader_schedule:
            current_leader : Leader = self.leader_schedule[block_number]
            if leader.campaign <= current_leader:
                raise ValueError

        self.leader_schedule[block_number] = leader
        # self.leader_lock.release()
        
    
    def get_leader_by_block_number(self, block_number: BlockNumber) -> Tuple[int, int]:
        """
        Returns a Leader object corresponding with the provided block number. If no
        leader exists for the provided block number, this function will return None.
        """

        if block_number in self.leader_schedule:
            return self.leader_schedule[block_number]
        
        return None

        
    
        
