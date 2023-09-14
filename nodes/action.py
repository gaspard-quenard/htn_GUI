from qtpy.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QScrollArea, QWidget, QFormLayout, QComboBox, QGroupBox
from qtpy.QtCore import Qt, QTimer
from calc_conf import register_node, OP_NODE_ACTION
from calc_node_base import CalcNode, CalcGraphicsNode
from nodeeditor.node_content_widget import QDMNodeContentWidget
from nodeeditor.utils import dumpException



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


# A subclass of QComboBox to handle mouse press events
class ColorChangingComboBox(QComboBox):
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        change_color()

    # def focusOutEvent(self, event):
    #     super().focusOutEvent(event)
    #     delayed_reset_color()

def delayed_reset_color():
    QTimer.singleShot(10, lambda: reset_color())

def delayed_change_color():
    QTimer.singleShot(10, lambda: change_color())









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

        edit = QLabel("Action_name")
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


@register_node(OP_NODE_ACTION)
class CalcNode_Input(CalcNode):
    icon = "icons/in.png"
    op_code = OP_NODE_ACTION
    op_title = "Action"
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