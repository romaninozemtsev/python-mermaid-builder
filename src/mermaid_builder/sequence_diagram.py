
from enum import Enum
from dataclasses import dataclass, field
from typing import Union


@dataclass
class Participant:
    id: str
    label: str = None

    def __str__(self) -> str:
        return f'{self.id} as {self.label}' if self.label else self.id


class ArrowType(Enum):
    SOLID_LINE_NO_ARROW = "->"
    DOTTED_LINE_NO_ARROW = "-->"
    SOLID_LINE_ARROW = "->>"
    DOTTED_LINE_ARROW = "-->>"
    SOLID_LINE_CROSS = "-x"
    DOTTED_LINE_CROSS = "--x"
    SOLID_LINE_OPEN_ARROW = "-)"
    DOTTED_LINE_OPEN_ARROW = "--)"

class ActivationMode(Enum):
    ACTIVATE = "+"
    DEACTIVATE = "-"
    NO_CHANGE = ""


@dataclass
class Message:
    src: Union[str, Participant]
    dest: Union[str, Participant]
    text: str = ""
    arrow: ArrowType = ArrowType.SOLID_LINE_NO_ARROW
    activation_mode: ActivationMode = ActivationMode.NO_CHANGE

    def __str__(self) -> str:
        src_id = str(self.src.id if isinstance(self.src, Participant) else self.src)
        dest_id = str(self.dest.id if isinstance(self.dest, Participant) else self.dest)
        return f'{src_id} {self.arrow.value}{self.activation_mode.value} {dest_id}: {self.text}'

class NotePosition(Enum):
    LEFT_OF = "left of"
    RIGHT_OF = "right of"
    OVER = "over"

@dataclass
class Note:
    participants: list[Union[str, Participant]]
    text: str
    position: NotePosition = NotePosition.OVER

    def __str__(self) -> str:
        actors = ",".join(str(p.id if isinstance(p, Participant) else p) for p in self.participants)
        return f'Note {self.position.value} {actors}: {self.text}'


@dataclass
class SequenceDiagram:
    participants: list = field(default_factory=list)
    messages: list = field(default_factory=list)
    notes: list = field(default_factory=list)

    def add_participant(self, actor: Union[str, Participant], label: str = None):
        if isinstance(actor, str):
            actor = Participant(actor, label)
        elif actor.label is None and label:
            actor.label = label

        self.participants.append(actor)
        return self

    def add_message(self, message: Message):
        self.messages.append(message)
        return self

    def add_message_between(self,
                            src: Union[str, Participant],
                            dest: Union[str, Participant],
                            text: str):
        self.messages.append(Message(src, dest, text))
        return self

    def add_note(self, note: Note):
        self.notes.append(note)
        return self

    def __str__(self) -> str:
        result = ["sequenceDiagram"]
        for participant in self.participants:
            result.append(f'  participant {participant}')
        for message in self.messages:
            result.append(f'  {message}')
        for note in self.notes:
            result.append(f'  {note}')
        return "\n".join(result)
