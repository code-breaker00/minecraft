from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# ------------------------------
# 📏 CONFIGURATION
MAP_SIZE = 30
VOID_Y = -10
keyboard_layout = 'azerty'  # ⌨️ Change à 'qwerty' si tu veux

# ------------------------------
# TEXTURES
grass_texture = load_texture('assets/grass.png')
stone_texture = load_texture('assets/stone.png')
brick_texture = load_texture('assets/brick.png')
dirt_texture = load_texture('assets/dirt.png')
sky_texture = load_texture('assets/skybox.png')
hand_texture = load_texture('assets/hand.png')

block_sound = Audio('assets/stone_hit.wav', autoplay=False)

# ------------------------------
# SKY + LUMIÈRE
sky = Sky()
sky.texture = sky_texture
DirectionalLight().look_at(Vec3(1, -1, -1))

# ------------------------------
# MAIN DU JOUEUR
hand = Entity(
    parent=camera.ui,
    model='quad',
    texture=hand_texture,
    scale=0.1,
    color=color.white,
    position=Vec2(0.6, -0.6)
)

# ------------------------------
# BLOCS
class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.white,
            scale=1
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                block_sound.play()
                Voxel(position=self.position + mouse.normal, texture=block_picker.texture)
            if key == 'right mouse down':
                block_sound.play()
                destroy(self)

# ------------------------------
# GÉNÉRATION DE LA MAP
def generate_map():
    for x in range(MAP_SIZE):
        for z in range(MAP_SIZE):
            Voxel(position=(x,0,z))

generate_map()

# ------------------------------
# JOUEUR
player = FirstPersonController()
player.gravity = 0.5
player.jump_height = 1
player.cursor.visible = True

# ------------------------------
# PICKER DE BLOCS
class BlockPicker(Entity):
    def __init__(self):
        super().__init__()
        self.textures = [grass_texture, stone_texture, brick_texture, dirt_texture]
        self.index = 0
        self.texture = self.textures[self.index]

    def input(self, key):
        if key == 'scroll up':
            self.index = (self.index + 1) % len(self.textures)
        if key == 'scroll down':
            self.index = (self.index - 1) % len(self.textures)
        self.texture = self.textures[self.index]

block_picker = BlockPicker()

# ------------------------------
# UI: GAME OVER
death_text = Text("GAME OVER", origin=(0,0), scale=2, color=color.red, enabled=False)
retry_button = Button(text='Rejouer', color=color.azure, scale=(0.2,0.1), y=-0.2, enabled=False)

def game_over():
    player.disable()
    hand.disable()
    death_text.enabled = True
    retry_button.enabled = True

def restart():
    death_text.enabled = False
    retry_button.enabled = False
    player.position = (MAP_SIZE//2, 2, MAP_SIZE//2)
    player.enable()
    hand.enable()

retry_button.on_click = restart

# ------------------------------
# UPDATE avec gestion QWERTY/AZERTY
def update():
    if player.y < VOID_Y and player.enabled:
        game_over()

    # Gestion du clavier AZERTY / QWERTY
    speed = 5 * time.dt
    if keyboard_layout == 'azerty': #modfie cette ligne 
        forward = 'z'; back = 's'; left = 'q'; right = 'd'
    else:
        forward = 'w'; back = 's'; left = 'a'; right = 'd'

    if held_keys[forward]: player.position += player.forward * speed
    if held_keys[back]:    player.position -= player.forward * speed
    if held_keys[left]:    player.position -= player.right * speed
    if held_keys[right]:   player.position += player.right * speed

app.run()
