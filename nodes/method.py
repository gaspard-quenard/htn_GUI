from qtpy.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QScrollArea, QWidget, QFormLayout, QComboBox, QGroupBox
from qtpy.QtCore import Qt, QTimer
from calc_conf import register_node, OP_NODE_METHOD
from calc_node_base import CalcNode, CalcGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException
from nodeeditor.node_edge import Edge, EDGE_TYPE_SQUARE, EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER



def updateGraph(index):
    print(f"New index {index}")

# Change the color of the given combo box and its related boxes
def change_color():
    color = "background-color: green;"  # set your desired color here
    for box in all_combo_boxes:
        box.blockSignals(True)
        box.setStyleSheet(color)
        box.blockSignals(False)


# Reset the color of the given combo box and its related boxes
def reset_color():
    default_style = ""  # default style (you can specify if needed)
    for box in all_combo_boxes:
        box.blockSignals(True)
        box.setStyleSheet(default_style)
        box.blockSignals(False)


def remove_combobox_from_list(combo_obj):
    all_combo_boxes.remove(combo_obj)


# A subclass of QComboBox to handle mouse press events
class ColorChangingComboBox(QComboBox):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        change_color()

    # def focusOutEvent(self, event):
    #     super().focusOutEvent(event)
    #     delayed_reset_color()


all_combo_boxes = []

def sync_comboboxes(index):
    # sender_box = sender()
    for box in all_combo_boxes:
        # if box != sender_box:
        box.blockSignals(True)
        box.setCurrentIndex(index)
        box.setStyleSheet("")
        box.blockSignals(False)

class CalcInputContent(QDMNodeContentWidget):

    def initUI(self):

        full_layout_action = QHBoxLayout(self)

        layout_action_preconditions = QVBoxLayout()
        layout_action_preconditions.addWidget(QLabel('Precondition'))
        layout_action_preconditions.addWidget(QLabel('at X L'))
        layout_action_preconditions.addWidget(QLabel('in P X'))
        layout_action_preconditions.addWidget(QLabel('road L L2'))




        layout_action_description = QVBoxLayout()

        edit = QLabel("Method_name")
        edit.setAlignment(Qt.AlignCenter)
        edit.setObjectName("test")

        # layout_params = QHBoxLayout()
        # layout_params.addWidget(QPushButton('1'))
        # layout_params.addWidget(QPushButton('2'))
        # layout_params.addWidget(QPushButton('3'))


        items = ["", "truck1", "truck2", "truck3", "truck4", "truck5"]


        all_params = QVBoxLayout()
        param1 = QHBoxLayout()
        param1.addWidget(QLabel('name: X'))
        param1.addWidget(QLabel('type: Truck'))
        possible_values_params1 = ColorChangingComboBox()
        possible_values_params1.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        possible_values_params1.addItems(items)
        possible_values_params1.currentIndexChanged.connect(sync_comboboxes)
        possible_values_params1.destroyed.connect(lambda: remove_combobox_from_list(possible_values_params1))
        param1.addWidget(possible_values_params1)

        param2 = QHBoxLayout()
        param2.addWidget(QLabel('name: Y'))
        param2.addWidget(QLabel('type: Truck'))
        possible_values_params2 = QComboBox()
        possible_values_params2.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        possible_values_params2.addItems(items)
        # possible_values_params2.currentIndexChanged.connect(sync_comboboxes)
        param2.addWidget(possible_values_params2)

        all_combo_boxes.append(possible_values_params1)
        # all_combo_boxes.append(possible_values_params2)

        all_params.addLayout(param1)
        all_params.addLayout(param2)



        layout_action_description.addWidget(edit)
        layout_action_description.addLayout(all_params)

        layout_action_effects = QVBoxLayout()
        layout_action_effects.addWidget(QLabel('Effects'))
        layout_action_effects.addWidget(QLabel('Eff1'))
        layout_action_effects.addWidget(QLabel('Eff2'))
        layout_action_effects.addWidget(QLabel('Eff3'))




        full_layout_action.addLayout(layout_action_preconditions)
        # full_layout_action.addStretch()
        full_layout_action.addLayout(layout_action_description)
        # full_layout_action.addStretch()
        full_layout_action.addLayout(layout_action_effects)

        # Add a button at the end with the text "Decompose" on it
        button = QPushButton("Decompose")
        button.clicked.connect(self.decompose)
        full_layout_action.addWidget(button)

        

    def serialize(self):
        res = super().serialize()
        # res['value'] = self.edit.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['value']
            # self.edit.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res
    
    def decompose(self):
        print("Decompose")

        try:
            # Creating two new nodes
            new_node1 = CalcNode_Input(self.node.scene)
            new_node1.setPos(self.node.pos.x(), self.node.pos.y() + 200)
            self.node.scene.history.storeHistory("Created node %s" % new_node1.__class__.__name__)

            new_node2 = CalcNode_Input(self.node.scene)
            new_node2.setPos(self.node.pos.x(), self.node.pos.y() - 200)
            self.node.scene.history.storeHistory("Created node %s" % new_node2.__class__.__name__)

            # For every edge connected to the input of the original node
            input_edges = list(self.node.inputs[0].edges)
            while input_edges:

                edge = input_edges.pop()
                # Get the node that's connected to the original one (source node)
                source_node = edge.start_socket.node
                if (source_node == self.node):
                    source_node = edge.end_socket.node

                # Get the output socket of this source node
                output_socket = source_node.outputs[0]

                # Create edges between this source node and both of the new nodes
                edge1 = Edge(self.node.scene, output_socket, new_node1.inputs[0], edge_type=EDGE_TYPE_DIRECT)
                edge2 = Edge(self.node.scene, output_socket, new_node2.inputs[0], edge_type=EDGE_TYPE_DIRECT)
                
                # Add the new edges to the scene
                # self.node.scene.addEdge(edge1)
                # self.node.scene.addEdge(edge2)

                # At the end, remove all the edges
                # Remove this edge from the scene too.
                edge.remove()


            # For every edge connected to the output of the original node
            output_edges = self.node.outputs[0].edges
            while output_edges:

                edge = output_edges.pop()
                # Get the node that's connected to the original one (source node)
                # Get the node that's connected to the original one (source node)
                destination_node = edge.start_socket.node
                if (destination_node == self.node):
                    destination_node = edge.end_socket.node

                # Get the output socket of this source node
                input_socket = destination_node.inputs[0]

                # Create edges between this new nodes and the destination node
                edge1 = Edge(self.node.scene, new_node1.outputs[0], input_socket, edge_type=EDGE_TYPE_DIRECT)
                edge2 = Edge(self.node.scene, new_node2.outputs[0], input_socket, edge_type=EDGE_TYPE_DIRECT)
                
                # Add the new edges to the scene
                # self.node.scene.addEdge(edge1)
                # self.node.scene.addEdge(edge2)

                # Remove this edge from the scene too.
                edge.remove()

            # Delete the original node
            self.node.remove()

        except Exception as e:
            dumpException(e)


@register_node(OP_NODE_METHOD)
class CalcNode_Input(CalcNode):
    icon = "icons/in.png"
    op_code = OP_NODE_METHOD
    op_title = "Method"
    content_label_objname = "calc_node_input"

    def __init__(self, scene):
        super().__init__(scene, inputs=[3], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = CalcInputContent(self)
        self.grNode = CalcGraphicsNode(self)
        # self.content.edit.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        # u_value = self.content.edit.text()
        # s_value = int(u_value)
        # self.value = s_value
        # self.markDirty(False)
        # self.markInvalid(False)

        # self.markDescendantsInvalid(False)
        # self.markDescendantsDirty()

        # self.grNode.setToolTip("")

        # self.evalChildren()

        return self.value