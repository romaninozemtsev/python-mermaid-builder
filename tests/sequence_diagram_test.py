import unittest

from mermaid_builder.sequence_diagram import SequenceDiagram, Participant, ArrowType, ActivationMode, Message, Note, NotePosition

class TestSequenceDiagram(unittest.TestCase):
    maxDiff = None
    def test_oop_style(self):
        diagram = SequenceDiagram()
        client = Participant(id='C', label='Client')
        server = Participant(id='S', label='Server')
        database = Participant(id='D', label='Database')
        (diagram
          .add_participant(client)
          .add_participant(server)
          .add_participant(database)
          .add_message(Message(src=client, dest=server, text='HTTP Request', activation_mode=ActivationMode.ACTIVATE))
          .add_message(Message(src=server, dest=database, text='SQL Query'))
          .add_message(Message(src=database, dest=server, text='Result', arrow=ArrowType.DOTTED_LINE_NO_ARROW))        
          .add_message(Message(src=server, dest=client, text='HTTP Response', activation_mode=ActivationMode.DEACTIVATE))
          .add_note(Note(participants=[client], text='This is a note', position=NotePosition.LEFT_OF)))
        expected = """sequenceDiagram
  participant C as Client
  participant S as Server
  participant D as Database
  C ->+ S: HTTP Request
  S -> D: SQL Query
  D --> S: Result
  S ->- C: HTTP Response
  Note left of C: This is a note"""
        self.assertEqual(str(diagram), expected)

if __name__ == '__main__':
    unittest.main()