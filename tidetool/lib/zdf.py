


from pathlib import Path
from typing import List
import re

class ZdfBlock:
    def __init__(self, type: str) -> None:
        # type of this block (eg; ZONE, TIDE_ZONE, TIDE_STATION)
        self.type = type

    def from_strings(self, strings: List[str]) -> None:
        """ Populates this ZdfBlock with the data contained in this list of strings. 
        """
        raise NotImplementedError(
            "ZdfBlock class must override from_strings function")

    def to_strings(self) -> List[str]:
        """ Converts this block into a list of strings formatted to match the CARIS
        format.
        """
        raise NotImplementedError("ZdfBlock class must override to_strings function")
    
    def __repr__(self) -> str:
       return f"type: {self.type}, len: {len(self.to_strings())}"


class ZdfUnparsed(ZdfBlock):
    """ ZdfUnparsed is a ZdfBlock implementation that will handle all blocks
    within a zdf file by simply preserving the data in a list of strings. It's
    to be used as a placeholder until a 'proper' ZdfBlock implementation is made.
    """

    def __init__(self, type: str) -> None:
        super().__init__(type)

        # list of unparsed lines that make up this block
        self.strings = []
    
    def from_strings(self, strings: List[str]) -> None:
        self.strings = strings
    
    def to_strings(self) -> List[str]:
        return self.strings


class ZdfTideStation(ZdfBlock):

    def __init__(self, type: str) -> None:
        super().__init__(type)
        # list of tuples, each tuple is
        #     (tide station name, lat, long, unknown float, unknown float, tide filename)
        self.data = []


    def from_strings(self, strings: List[str]) -> None:
        for s in strings:
            s_bits = s.split(',')
            d = (
                s_bits[0],
                float(s_bits[1]),
                float(s_bits[2]),
                float(s_bits[3]),
                float(s_bits[4]),
                s_bits[5]
            )
            self.data.append(d)


    def to_strings(self) -> List[str]:
        lines = [
            f"{d[0]},{d[1]},{d[2]},{d[3]},{d[4]},{d[5]}"
            for d in self.data
        ]
        return lines


def block_for_type(type: str) -> ZdfBlock:
    if type == 'TIDE_STATION':
        return ZdfTideStation(type)
    else:
        return ZdfUnparsed(type)


class ZoneDefinitionFile:
    """ Model definition for a CARIS zone defintion file (.zdf).

    A zdf file is broken down into a number of blocks, each block represents 
    a zone `[ZONE]` , tide zone `[TIDE_ZONE]`, `[TIDE_STATION]` or similar.
    The specifics for each block are handled by an implementation of the
    ZdfBlock class.
    """

    def __init__(self, filename) -> None:
        self.filename = filename
        self.blocks=[]

    
    def add_block(self, block: ZdfBlock) -> None:
        self.blocks.append(block)


class ZdfParser:

    def __init__(self) -> None:
        self.zdf = None

    def _get_type(self, line:str) -> str:
        result = re.search(r'\[(.*?)\]', line)
        
        if result is None:
            # no match, not a type line
            raise RuntimeError("Not a type line, expected something like \"[ZONE]\"")

        return result.groups()[0]

    def _get_block(self, block_type: str, lines: List[str]) -> ZdfBlock:
        block = block_for_type(block_type)
        block.from_strings(lines)
        return block

    def _process_lines(self, lines: List[str]) -> None:
        

        type = None
        block_lines = None

        for (i, line) in enumerate(lines):
            
            if line.startswith('['):
                if block_lines is not None:
                    block = self._get_block(type, block_lines)
                    self.zdf.add_block(block)

                type = self._get_type(line)
                block_lines = []
            elif len(line.strip()) == 0:
                # skip over blank lines
                pass
            else:
                block_lines.append(line)

        block = self._get_block(type, block_lines)
        self.zdf.add_block(block)


    def read(self, path: Path) -> ZoneDefinitionFile:
        self.zdf = ZoneDefinitionFile(path)

        with path.open('r') as file:
            lines = file.read().splitlines()

