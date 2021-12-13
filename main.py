import math
from random import randint, random

import pygame

TAUSTAVARI = (180, 180, 240)  # (Red, Green, Blue), 0...255
FPS = 60  # frames per second

def main():
    peli = Peli()
    peli.aja()


class Peli:
    def __init__(self):
        self.ajossa = True
        self.naytto = None
        self.leveys = 1280
        self.korkeus = 720
        self.nayton_koko = (self.leveys, self.korkeus)
 
    def aja(self):
        self.alustus()
        while self.ajossa:
            for event in pygame.event.get():
                self.tapahtuma(event)
            self.pelilogiikka()
            self.renderointi()
        self.lopetus()

    def alustus(self):
        pygame.init()
        self.kello = pygame.time.Clock()
        self.kokoruutu = False
        self.naytto = pygame.display.set_mode(
            self.nayton_koko, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.raketti_iso = pygame.image.load("millennium-falcon.png")
        self.raketti_pieni = pygame.transform.rotozoom(self.raketti_iso, 0, 0.15)
        self.juttu_iso = pygame.image.load("astronaut.png")
        self.juttu_pieni = pygame.transform.rotozoom(self.juttu_iso, 0, 0.12)
        self.raketin_kulma = 0
        self.raketin_pyorimisvauhti = 0
        self.raketin_sijainti = (400, 300)
        self.arvo_uusi_juttu()
        self.vauhti = 0
        self.hiiren_nappi_pohjassa = False
        self.voima = 0
        self.voimanlisays = False
        self.laukaisu = False
        self.pisteet = 0
        self.aikaa_jaljella = 20 * FPS

    def arvo_uusi_juttu(self):        
        self.jutun_kulma = 0
        self.jutun_pyorimisvauhti = random() - 0.5
        self.jutun_sijainti = (randint(0, self.leveys), randint(0, self.korkeus))

    def tapahtuma(self, event):
        if event.type == pygame.QUIT:
            self.ajossa = False
        # Hiiren tapahtumat --------------------------------------
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.hiiren_nappi_pohjassa = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.hiiren_nappi_pohjassa = False
        # Näppäimen painaminen alas ------------------------------
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.raketin_pyorimisvauhti = 3
            elif event.key == pygame.K_RIGHT:
                self.raketin_pyorimisvauhti = -3
            elif event.key == pygame.K_SPACE:
                self.voimanlisays = True
        # Näppäimen nosto ylös  ----------------------------------
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.ajossa = False
            elif event.key == pygame.K_F11:
                self.vaihda_kokoruututila()
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.raketin_pyorimisvauhti = 0
            elif event.key == pygame.K_SPACE:
                self.voimanlisays = False
                self.laukaisu = True           

    def pelilogiikka(self):
        if self.aikaa_jaljella > 0:
            self.aikaa_jaljella -= 1
        else:
            return

        if self.hiiren_nappi_pohjassa:
            self.raketin_sijainti = pygame.mouse.get_pos()

        if self.raketin_pyorimisvauhti != 0:
            self.raketin_kulma = (self.raketin_kulma + self.raketin_pyorimisvauhti) % 360

        if self.jutun_pyorimisvauhti != 0:
            self.jutun_kulma = (self.jutun_kulma + self.jutun_pyorimisvauhti) % 360

        if self.voimanlisays:
            self.voima = min(self.voima + 2, 100)

        if self.laukaisu:
            self.vauhti = self.voima ** 2 / 200.0
            self.voima = 0
            self.laukaisu = False

        if self.vauhti > 0.1:
            vauhti_x = -self.vauhti * math.sin(self.raketin_kulma / 180 * math.pi)
            vauhti_y = -self.vauhti * math.cos(self.raketin_kulma / 180 * math.pi)
            uusi_x = self.raketin_sijainti[0] + vauhti_x
            uusi_y = self.raketin_sijainti[1] + vauhti_y
            self.raketin_sijainti = (uusi_x, uusi_y)
            self.vauhti *= 0.97

        etaisyys_2 = (
            (self.raketin_sijainti[0] - self.jutun_sijainti[0])**2 +
            (self.raketin_sijainti[1] - self.jutun_sijainti[1])**2)
        if etaisyys_2 < 5000:
            self.pisteet += 1
            self.aikaa_jaljella += 2 * FPS
            self.arvo_uusi_juttu()

    def renderointi(self):
        # Tausta
        self.naytto.fill(TAUSTAVARI)
        # Juttu
        kuva = pygame.transform.rotozoom(self.juttu_pieni, self.jutun_kulma, 1)
        laatikko = kuva.get_rect(center=self.jutun_sijainti)
        self.naytto.blit(kuva, laatikko.topleft)
        # Raketti
        kuva = pygame.transform.rotozoom(self.raketti_pieni, self.raketin_kulma, 1)
        laatikko = kuva.get_rect(center=self.raketin_sijainti)
        self.naytto.blit(kuva, laatikko.topleft)
        # Voimapalkki
        pygame.draw.rect(self.naytto, (0, 0, 0), (2, self.korkeus - 19, 102, 17))
        pygame.draw.rect(self.naytto, (0, 255, 0), (3, self.korkeus - 18, self.voima, 15))
        # Suuntapallo
        suuntapallo_x = self.leveys - 35
        suuntapallo_y = self.korkeus - 35
        suuntavektori_x = -30 * math.sin(self.raketin_kulma / 180 * math.pi)
        suuntavektori_y = -30 * math.cos(self.raketin_kulma / 180 * math.pi)
        pygame.draw.circle(self.naytto, (0, 0, 0), (suuntapallo_x, suuntapallo_y), 30)
        pygame.draw.line(self.naytto, (255, 0, 0),
                        (suuntapallo_x, suuntapallo_y),
                        (suuntapallo_x + suuntavektori_x, suuntapallo_y + suuntavektori_y))
        # Pisteet
        fontti = pygame.font.Font("font/SyneMono-Regular.ttf", 32)
        teksti_kuva = fontti.render(f"Pisteet:{self.pisteet:3}", True, (128, 0, 128))
        self.naytto.blit(teksti_kuva, (self.leveys - teksti_kuva.get_width() - 10, 10))
        # Aika
        fontti = pygame.font.Font("font/SyneMono-Regular.ttf", 32)
        teksti_kuva = fontti.render(f"Aika:{self.aikaa_jaljella:3}", True, (128, 0, 128))
        self.naytto.blit(teksti_kuva, (10, 10))
        # Loppu teksti
        if self.aikaa_jaljella <= 0:
            fontti = pygame.font.Font("font/SyneMono-Regular.ttf", 96)
            teksti_kuva = fontti.render("GAME OVER!", True, (128, 0, 128))
            self.naytto.blit(teksti_kuva, (
                (self.leveys - teksti_kuva.get_width()) / 2,
                (self.korkeus - teksti_kuva.get_height()) / 2))
        # Päivitä ruutu
        pygame.display.flip()
        self.kello.tick(FPS)

    def vaihda_kokoruututila(self):
        self.kokoruutu = not self.kokoruutu
        if self.kokoruutu:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode(self.nayton_koko)
        naytto = pygame.display.get_surface()
        self.leveys = naytto.get_width()
        self.korkeus = naytto.get_height()

    def lopetus(self):
        pygame.quit()
 

if __name__ == "__main__" :
    main()