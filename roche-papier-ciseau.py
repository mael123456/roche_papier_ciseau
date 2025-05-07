"""
programme fait par mael chassin de kergommeaux
goupe 123
description : jeu de roche papier ciseau
"""

import arcade
import random
from attack_animation import *
from game_state import GameState

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "roche papier ciseau"


class MyGame(arcade.Window):
    """

    La classe principale de l'application

    NOTE: Vous pouvez effacer les méthodes que vous n'avez pas besoin.
    Si vous en avez besoin, remplacer le mot clé "pass" par votre propre code.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.BLACK)
        self.player_attack_type = {
            AttackType.ROCK: False,
            AttackType.PAPER: False,
            AttackType.SCISSORS: False
        }
        # Si vous avez des listes de sprites, il faut les créer ici et les
        # initialiser à None.
        # variable qui sert a determiner le gagnant pour ensuite afficher le texte
        self.gagant = 0
        self.status = False
        # les variables qui gere les des joueurs
        self.nb_choix = -1
        self.pt_joueur = 0
        self.pt_ordi = 0
        self.choix_joueur = ''
        self.choix_ordi = ''
        self.flag = False
        self.game_state = GameState.NOT_STARTED


    def setup(self):
        """
        Configurer les variables de votre jeu ici. Il faut appeler la méthode une nouvelle
        fois si vous recommencer une nouvelle partie.
        """
        # C'est ici que vous allez créer vos listes de sprites et vos sprites.
        # C'est aussi ici que vous charger les sons de votre jeu.
        self.game_sprite_rock = arcade.SpriteList()
        self.game_sprite_paper = arcade.SpriteList()
        self.game_sprite_cisor = arcade.SpriteList()
        self.base_sprite = arcade.SpriteList()
        self.pc_sprite = arcade.SpriteList()
        self.pc_rock = AttackAnimation(AttackType.ROCK, 575, 175)
        self.pc_sprite_rock = arcade.SpriteList()
        self.pc_paper = AttackAnimation(AttackType.PAPER, 575, 175)
        self.pc_sprite_paper = arcade.SpriteList()
        self.pc_cisor = AttackAnimation(AttackType.SCISSORS, 575, 175)
        self.pc_sprite_cisor = arcade.SpriteList()
        self.pc_sprite_paper.append(self.pc_paper)
        self.pc_sprite_rock.append(self.pc_rock)
        self.pc_sprite_cisor.append(self.pc_cisor)

        self.rock = AttackAnimation(AttackType.ROCK,150,175)
        self.cisor = AttackAnimation(AttackType.SCISSORS,225,175)
        self.paper = AttackAnimation(AttackType.PAPER,300,175)
        ordinateur = arcade.Sprite("assets/compy.png", 1, 575, 250)
        visage = arcade.Sprite("assets/faceBeard.png", .22, 225, 250)
        self.game_sprite_cisor.append(self.cisor)
        self.game_sprite_paper.append(self.paper)
        self.game_sprite_rock.append(self.rock)
        self.base_sprite.append(ordinateur)
        self.base_sprite.append(visage)

    def on_draw(self):

        # Cette commande permet d'effacer l'écran avant de dessiner. Elle va dessiner l'arrière
        # plan selon la couleur spécifié avec la méthode "set_background_color".
        self.clear()
        self.base_sprite.draw()
        # dessin des bases du jeu qui sont tout le temps afficher
        arcade.draw_lbwh_rectangle_outline(125,150,50,50,arcade.color.RED)
        arcade.draw_lbwh_rectangle_outline(200, 150, 50, 50, arcade.color.RED)
        arcade.draw_lbwh_rectangle_outline(275, 150, 50, 50, arcade.color.RED)
        arcade.draw_lbwh_rectangle_outline(550, 150, 50, 50, arcade.color.RED)
        arcade.draw_text('ROCHE, PAPIER, CISEAU', 100, 500, arcade.color.RED, 50)
        arcade.draw_text('le pointage du joueur est : ' + str(self.pt_joueur), 50, 100, arcade.color.RED, 20)
        arcade.draw_text('le pointage de lordinateur est : ' + str(self.pt_ordi), 400, 100, arcade.color.RED, 20)

        if self.game_state == GameState.NOT_STARTED:
            arcade.draw_text('APPUYER SUR ESPACE POUR COMMENCER LE JEU', 150, 430, arcade.color.RED, 17)
        elif self.game_state == GameState.GAME_OVER:
            if self.pt_joueur >= 3:
                arcade.draw_text('FIN DE LA PARTIE, LE JOUEUR A GAGNER, APPUYER SUR ESPACE POUR RECOMMENCER', 20, 430, arcade.color.RED, 17)
            elif self.pt_ordi >= 3:
                arcade.draw_text('FIN DE LA PARTIE, LORDI A GAGNER, APPUYER SUR ESPACE POUR RECOMMENCER', 20, 430, arcade.color.RED, 17)
        elif self.game_state == GameState.ROUND_DONE:
            arcade.draw_text('ROUND DONE, APPUYER SUR ESPACE POUR RECOMMENCER', 20, 430, arcade.color.RED, 17)
        elif not self.status:
            if self.gagant == 3:
                arcade.draw_text('EGALITER, APPUYER SUR ESPACE POUR CONTINUER', 20, 430, arcade.color.RED, 17)
            elif self.gagant == 1:
                arcade.draw_text('LE JOUEUR A GAGNER LA RONDE, APPUYER SUR ESPACE POUR CONTINUER', 20, 430, arcade.color.RED, 17)
            elif self.gagant == 2:
                arcade.draw_text('LORDINATEUR A GAGNER LA RONDE, APPUYER SUR ESPACE POUR CONTINUER', 20, 430, arcade.color.RED, 17)
        # Invoquer la méthode "draw()" de vos sprites ici.
        if self.game_state == GameState.ROUND_ACTIVE:
            if self.status:
                self.game_sprite_rock.draw()
                self.game_sprite_paper.draw()
                self.game_sprite_cisor.draw()
            else:
                if self.choix_joueur == 'rock':
                    self.game_sprite_rock.draw()
                elif self.choix_joueur == 'paper':
                    self.game_sprite_paper.draw()
                if self.choix_joueur == 'cisor':
                    self.game_sprite_cisor.draw()
            #self.game_sprite.draw()
            if self.choix_ordi == 'roche':
                self.pc_sprite_rock.draw()
            elif self.choix_ordi == 'paper':
                self.pc_sprite_paper.draw()
            elif self.choix_ordi == 'cisor':
                self.pc_sprite_cisor.draw()

    def on_update(self, delta_time):
        """
        Toute la logique pour déplacer les objets de votre jeu et de
        simuler sa logique vont ici. Normalement, c'est ici que
        vous allez invoquer la méthode "update()" sur vos listes de sprites.
        Paramètre:
            - delta_time : le nombre de milliseconde depuis le dernier update.
        """
        self.rock.on_update()
        self.paper.on_update()
        self.cisor.on_update()
        if self.choix_ordi == 'roche':
            self.pc_rock.on_update()
        elif self.choix_ordi == 'paper':
            self.pc_paper.on_update()
        elif self.choix_ordi == 'cisor':
            self.pc_cisor.on_update()

    def on_key_press(self, key, key_modifiers):
        """
        Cette méthode est invoquée à chaque fois que l'usager tape une touche
        sur le clavier.
        Paramètres:
            - key: la touche enfoncée
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?

        Pour connaître la liste des touches possibles:
        http://arcade.academy/arcade.key.html
        """

        if key == arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED:
                self.status = True
                self.flag = False
                self.pt_joueur = 0
                self.pt_ordi = 0
                self.gagant = 0
                self.game_state = GameState.ROUND_ACTIVE
                # mettre les pointage a zero
            elif self.game_state == GameState.ROUND_DONE:
                self.status = True
                self.game_state = GameState.ROUND_ACTIVE
                self.choix_ordi = ''
                # pour verifier le fonctionnement
                if self.pt_ordi >= 3 or self.pt_joueur >= 3:
                    self.game_state = GameState.GAME_OVER
                else:
                    print('start')
                    self.game_state = GameState.ROUND_ACTIVE
                    self.flag = False
                # mettre les pointage a zero
            elif self.game_state == GameState.GAME_OVER:
                self.status = True
                self.flag = False
                self.choix_ordi = ''
                self.pt_joueur = 0
                self.pt_ordi = 0
                self.gagant = 0
                self.game_state = GameState.ROUND_ACTIVE
                # mettre les pointage a zero
            elif not self.status:
                if self.pt_ordi >= 3 or self.pt_joueur >= 3:
                    self.game_state = GameState.GAME_OVER
                else:
                    self.game_state = GameState.ROUND_DONE
                print('round done')

            print(self.game_state)

    def computer_chose(self):

        # choix aleatoire de loutil de lordinateur

        self.nb_choix = random.randint(1,3)
        if self.nb_choix == 1:
            self.choix_ordi = 'roche'
            print('pc_rock')
        elif self.nb_choix == 2:
            self.choix_ordi = 'paper'
            print('pc_paper')
        elif self.nb_choix == 3:
            self.choix_ordi = 'cisor'
            print('pc_cisor')

        if self.choix_ordi == 'roche' and self.choix_joueur == 'roche':
            self.gagant = 3
            self.status = False
        elif self.choix_ordi == 'paper' and self.choix_joueur == 'paper':
            self.gagant = 3
            self.status = False
        elif self.choix_ordi == 'cisor' and self.choix_joueur == 'cisor':
            self.gagant = 3
            self.status = False
        elif self.choix_ordi == 'paper' and self.choix_joueur == 'cisor':
            self.pt_joueur += 1
            self.gagant = 1
            self.status = False
        elif self.choix_ordi == 'paper' and self.choix_joueur == 'rock':
            self.pt_ordi += 1
            self.gagant = 2
            self.status = False
        elif self.choix_ordi == 'cisor' and self.choix_joueur == 'paper':
            self.pt_ordi += 1
            self.gagant = 2
            self.status = False
        elif self.choix_ordi == 'cisor' and self.choix_joueur == 'rock':
            self.pt_joueur += 1
            self.gagant = 1
            self.status = False
        elif self.choix_ordi == 'roche' and self.choix_joueur == 'paper':
            self.pt_joueur += 1
            self.gagant = 1
            self.status = False
        elif self.choix_ordi == 'roche' and self.choix_joueur == 'cisor':
            self.pt_ordi += 1
            self.gagant = 2
            self.status = False

    def on_mouse_press(self, x, y, button, key_modifiers):

        """
        Méthode invoquée lorsque l'usager clique un bouton de la souris.
        Paramètres:
            - x, y: coordonnées où le bouton a été cliqué
            - button: le bouton de la souris appuyé
            - key_modifiers: est-ce que l'usager appuie sur "shift" ou "ctrl" ?
        """
        if not self.flag:
            if self.rock.collides_with_point((x, y)):
                print('roche toucher')
                self.choix_joueur = 'rock'
                self.flag = True
                self.computer_chose()
            elif self.cisor.collides_with_point((x, y)):
                print('ciseau toucher')
                self.choix_joueur = 'cisor'
                self.flag = True
                self.computer_chose()
            elif self.paper.collides_with_point((x, y)):
                print('papier toucher')
                self.choix_joueur = 'paper'
                self.flag = True
                self.computer_chose()


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
