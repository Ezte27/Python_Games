import pygame, os
from settings import *
from timer import Timer

class Menu:
    def __init__(self, player, toggle_menu) -> None:
        
        # General Setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(f"{os.getcwd()}{FONT_PATH}", FONT_SIZE)

        self.setup()

        # Movement
        self.move_index = 0
        self.options_len = len(SHOP_OPTIONS)
        self.trade_option = 0 # 0 = BUY, 1 = SELL

        # Timers
        self.move_timer = Timer(200)

    def setup(self):

        # Create text surfaces
        self.text_surfs = []
        self.total_height = 0
        for item in SHOP_OPTIONS:
            item = item.replace('_', ' ', 1) # Change underscore '_' to a space ' ' so that corn_seeds -> corn seeds
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (MENU_PADDING * 2)
        
        self.total_height += (len(self.text_surfs) - 1) * MENU_SPACE
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - MENU_WIDTH / 2, self.menu_top, MENU_WIDTH, self.total_height)

        # Buy / Sell Surface
        self.buy_text = self.font.render('Buy', False, 'Black')
        self.sell_text = self.font.render('Sell', False, 'Black')

    def display_money(self):
        text_surf = self.font.render(f"${self.player.money}", False, 'Black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, "White", text_rect.inflate(10, 10), 0, 6)
        self.display_surface.blit(text_surf, text_rect)

    def show_entry(self, text_surf, amount, top, selected):

        # Background
        bg_rect = pygame.Rect(self.main_rect.left, top, MENU_WIDTH, text_surf.get_height() + (MENU_PADDING * 2))
        pygame.draw.rect(self.display_surface, "White", bg_rect, 0, 4)

        # Text 
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # Amount Surface
        amount_surf = self.font.render(str(amount), False, "Black")
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        # Selected
        if selected:
            pygame.draw.rect(self.display_surface, 'Black', bg_rect, 4, 4)
            if self.trade_option == 0: # Buy
                pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 250, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)
            elif self.trade_option == 1: # Sell
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 250, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()
        
        # Select Movement
        if not self.move_timer.active:
            if keys[pygame.K_UP]:
                self.move_timer.activate()
                self.move_index -= 1
                self.move_index = self.options_len - 1 if self.move_index < 0 else self.move_index
            
            elif keys[pygame.K_DOWN]:
                self.move_timer.activate()
                self.move_index += 1
                self.move_index = 0 if self.move_index + 1 > self.options_len else self.move_index

            elif keys[pygame.K_SPACE]: # Change Trade Option ( BUY or SELL )
                self.move_timer.activate()

                self.trade_option = 0 if self.trade_option == 1 else 1

            elif keys[pygame.K_RETURN]: # The player hits ENTER
                self.move_timer.activate()

                current_item = SHOP_OPTIONS[self.move_index]
                
                # Buy
                if self.trade_option == 0:
                    price = PURCHASE_PRICES[current_item]
                    if self.player.money >= price:
                        self.player.inventory[current_item] += 1
                        self.player.money -= price

                # Sell
                elif self.trade_option == 1: 
                    if self.player.inventory[current_item] > 0:
                        self.player.inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]

    def update(self):

        # Entries
        amount_list = list(self.player.inventory.values())
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (MENU_PADDING * 2) + MENU_SPACE)
            self.show_entry(text_surf, amount_list[text_index], top, (text_index == self.move_index))

        # Money
        self.display_money()

        # Timers
        self.move_timer.update()

        self.input()