import pygame

TAUSTAVARI = (180, 180, 240)  # (Red, Green, Blue), 0...255


def main():
    peli = Peli()
    peli.aja()


class Peli:
    def __init__(self):
        self.ajossa = True
        self.naytto = None
        self.leveys = 800
        self.korkeus = 600
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
        self.naytto = pygame.display.set_mode(
            self.nayton_koko, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.kuva_iso = pygame.image.load("millennium-falcon.png")
        self.kuva_pieni = pygame.transform.rotozoom(self.kuva_iso, 0, 0.15)
        self.kulma = 0
        self.sijainti = (400, 300)
        self.nappi_pohjassa = False

    def tapahtuma(self, event):
        if event.type == pygame.QUIT:
            self.ajossa = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.nappi_pohjassa = True
            self.sijainti = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:
            self.nappi_pohjassa = False

    def pelilogiikka(self):
        if self.nappi_pohjassa == True:
            self.sijainti = pygame.mouse.get_pos()
        self.kulma = (self.kulma - 3) % 360
        #self.kulma -= 3 --> Ei hyvä! 

    def renderointi(self):
        self.naytto.fill(TAUSTAVARI)  # (Red, Green, Blue)
        kuva = pygame.transform.rotozoom(self.kuva_pieni, self.kulma, 1)
        laatikko = kuva.get_rect(center=(self.sijainti))
        self.naytto.blit(kuva, laatikko.topleft)
        pygame.display.flip()
        self.kello.tick(60)  # 60 fps (frames per second)

    def lopetus(self):
        pygame.quit()
 

if __name__ == "__main__" :
    main()
