# Nome: Joao Roizen Fontana
# Matricula: 1710431

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
from math import cos, sin
import numpy

# Parâmetros iniciais
rotation_speed_earth = 0.5
rotation_speed_moon = 1.0
translation_speed_earth = 0.1
translation_speed_mercury = 0.4

# Angulos iniciais
angle_earth = 0.0
angle_moon = 0.0
angle_mercury = 0.0

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

def load_texture(file_path):
    image = Image.open(file_path)
    image_data = numpy.array(list(image.getdata()), numpy.uint8)
    texture_id = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id

def draw_circle(radius, texture=None):
    glBegin(GL_POLYGON)
    for i in range(100):
        theta = 2.0 * 3.1415926 * i / 100
        x = radius * cos(theta)
        y = radius * sin(theta)
        glTexCoord2f((x + 1) / 2, (y + 1) / 2)
        glVertex2f(x, y)
    glEnd()

def draw_background():
    glBindTexture(GL_TEXTURE_2D, texture_background)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex2f(-1.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex2f(-1.0, 1.0)
    glTexCoord2f(1.0, 1.0); glVertex2f(1.0, 1.0)
    glTexCoord2f(1.0, 0.0); glVertex2f(1.0, -1.0)
    glEnd()

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Desenha o fundo
    glBindTexture(GL_TEXTURE_2D, texture_background)
    draw_background()

    # Desenha o Sol
    glBindTexture(GL_TEXTURE_2D, texture_sun)
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(0.2)

    # Desenha Mercúrio
    glPushMatrix()
    glRotatef(angle_mercury, 0.0, 0.0, 1.0)
    glTranslatef(0.5, 0.0, 0.0)
    glBindTexture(GL_TEXTURE_2D, texture_mercury)
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(0.05)
    glPopMatrix()

    # Desenha a Terra
    glPushMatrix()
    glRotatef(angle_earth, 0.0, 0.0, 1.0)
    glTranslatef(0.8, 0.0, 0.0)
    glBindTexture(GL_TEXTURE_2D, texture_earth)
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(0.1)

    # Desenha a Lua
    glPushMatrix()
    glRotatef(angle_moon, 0.0, 0.0, 1.0)
    glTranslatef(0.2, 0.0, 0.0)
    glBindTexture(GL_TEXTURE_2D, texture_moon)
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(0.03)
    glPopMatrix()

    glPopMatrix()

    glutSwapBuffers()

def update(value):
    global angle_earth, angle_moon, angle_mercury

    # Atualiza os ângulos
    angle_earth += rotation_speed_earth
    angle_moon += rotation_speed_moon
    angle_mercury += translation_speed_mercury

    # Redesenha a cena
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(800, 800)
    glutCreateWindow(b'Mini Sistema Solar')

    glEnable(GL_TEXTURE_2D)
    global texture_background, texture_sun, texture_earth, texture_moon, texture_mercury

    # Carrega as texturas
    texture_background = load_texture("Projeto1/imagens/space_texture.jpg")
    texture_sun = load_texture("Projeto1/imagens/sun_texture.jpg")
    texture_earth = load_texture("Projeto1/imagens/earth_texture.jpg")
    texture_moon = load_texture("Projeto1/imagens/moon_texture.jpg")
    texture_mercury = load_texture("Projeto1/imagens/mercury_texture.jpg")

    glutDisplayFunc(draw_scene)
    glutTimerFunc(25, update, 0)

    init()
    glutMainLoop()

if __name__ == "__main__":
    main()
