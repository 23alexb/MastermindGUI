#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Graphic User Interface for Mastermind Desktop game

@author: alexbrebner
"""

import wx
import wx.lib.agw.gradientbutton as gb
import random

class UI(wx.Frame):
    
    def __init__(self, *args, **kwargs):
        
        # Create frame and panel
        wx.Frame.__init__(self, None)
        self.pnl = wx.Panel(self, -1)
        
        # Initialize UI and dictionaries of buttons colours/positions/sizes
        self.SetGameDefaults()
        self.ReferenceDicts()
        self.InitUI()
        
        # Create buttons
        self.GameScreen_Create()
        
    # ***************************************************************************************************
    # INITIALIZE*********************************************************************************
    # ***************************************************************************************************

    def SetGameDefaults(self):
        # Defaults relating to code length
        self.code_length = 4
        self.min_code_length = 3
        self.max_code_length = 6
        
        # Defaults relating to doubles/triples/etc.
        self.multiples = 'Off'
        self.max_instance_of_each_colour = 1
        
        # Defaults relating to guess qty and scrolling
        self.this_turn = 1
        self.max_guesses = 0
        self.max_guesses_displayed = 6
        self.scroll_on = False
        self.scroll_up_on = False
        self.scroll_down_on = False
        self.scroll_index = 0
        
    def ReferenceDicts(self):
        # Possible colours
        self.colours = [ 'red', 'orange', 'yellow', 'green',
                         'blue', 'violet', 'purple', 'pink' ]
                         
        # Size constants
        peg_size = 60
        response_size = peg_size / 2
        spacer_1 = 10
        spacer_2 = 5
        div_x = 2
        turn_x = peg_size * 1
        self.peg_size = peg_size
        self.spacer_1 = spacer_1
        self.spacer_2 = spacer_2
        buffer = (self.max_code_length - self.code_length) * (peg_size + spacer_2) / 2
        
        # Size calculations
        answer_bar_x = peg_size * 4 + response_size + spacer_2 * 6
        guess_bar_x = answer_bar_x - spacer_2 * 2 + spacer_1 * 2
        guess_bar_y = spacer_1 * 3 + peg_size * 3 / 2
        previous_guess_bar_x = spacer_2 * 2 + peg_size
        previous_guess_bar_y = spacer_2 * 2 + peg_size
        frame_x = spacer_1 * 2 + peg_size * self.max_code_length + turn_x + guess_bar_x + spacer_1 * 2 + spacer_2
        frame_y = max(spacer_1 * 3 + self.max_guesses_displayed * (peg_size + spacer_2) + spacer_2 + peg_size * 1.75,
                      peg_size * 6.5 + spacer_1 * 6 + spacer_2 * 5)
        
        # Size dict
        s = { 'frame_default' : (frame_x + spacer_1, frame_y + spacer_1),
              'guess_bar' : (guess_bar_x, guess_bar_y),
              'previous_guess_bar' : (previous_guess_bar_x, previous_guess_bar_y),
              'peg' : (peg_size, peg_size),
              'peg_active' : (peg_size * 4 + spacer_2 * 3, peg_size),
              'scroll' : (peg_size/2, (peg_size - spacer_2) / 2),
              'response' : ((peg_size - spacer_2) / 2, (peg_size - spacer_2) / 2),
              'submit' : ((peg_size + spacer_2) * self.code_length - spacer_2, peg_size / 2),
              'btn_sml' : (peg_size * 2 + spacer_2, peg_size / 2),
              'btn_med' : (peg_size * 4 + spacer_2 * 3, peg_size * 3 / 4),
              'btn_option' : (peg_size, peg_size / 2),
              'turn' : (turn_x, peg_size / 2),
              'div' : (div_x, frame_y * 2)
             }
        self.control_sizes_dict = s
        
        # Position calculations
        peg_x = spacer_1
        new_game_y = spacer_1
        restart_y = new_game_y + peg_size * 3 / 4 + spacer_2
        active_peg_y = restart_y + spacer_1 + s['btn_med'][1]
        peg_y = active_peg_y + spacer_1 + peg_size
        div_x = spacer_1 + s['btn_med'][0] + spacer_1
        turn_btn_x = div_x + spacer_1 + buffer
        guess_peg_x = div_x + s['div'][0] + spacer_1 + buffer + s['turn'][0] + spacer_2
        game_info_y = peg_y + peg_size * 2 + spacer_1 + spacer_2
        prev_guess_peg_y = spacer_1 * 3 + peg_size * 2.5
        scroll_x = guess_peg_x + peg_size * self.code_length + spacer_2 * (self.code_length - 1) + spacer_1
        turn_btn_x = div_x + spacer_1 + buffer
        turn_btn_y = 0 # Placeholder - value will be equal to applicable guess peg y value
        turn_offset_x = 1#s['turn'][0] / 2
        turn_offset_y = s['turn'][1] / 4
        restxt_offset_x = s['btn_sml'][0] / 3.3
        restxt_offset_y = s['btn_sml'][1] / 4
        
        # Position dict
        p = { 'code_length' : (spacer_1, game_info_y),
              'code_length_2' : (spacer_1 + (peg_size + spacer_2) * 2, game_info_y),
              'code_length_text_offset' : (peg_size / 2 - 7, 6),
              'multis' : (spacer_1, game_info_y + s['btn_sml'][1] + spacer_2),
              'multis_2' : (spacer_1 + (peg_size + spacer_2) * 2, game_info_y + s['btn_sml'][1] + spacer_2),
              'multis_text_offset' : (peg_size / 2 - 10, 6),
              'palette' : (spacer_1, game_info_y + (s['btn_sml'][1] + spacer_2) * 2),
              'give_up' : (spacer_1, game_info_y + (s['btn_sml'][1] + spacer_2) * 3),
              'btn_newgame' : (spacer_1, new_game_y), 
              'btn_restartgame' : (spacer_1, restart_y),
              'peg_red' : (peg_x, peg_y),
              'peg_orange' : (peg_x + (peg_size + spacer_2), peg_y),
              'peg_yellow' : (peg_x + (peg_size + spacer_2) * 2, peg_y),
              'peg_green' : (peg_x + (peg_size + spacer_2) * 3, peg_y),
              'peg_blue' : (peg_x, peg_y + peg_size + spacer_2),
              'peg_violet' : (peg_x + (peg_size + spacer_2), peg_y + peg_size + spacer_2),
              'peg_purple' : (peg_x + (peg_size + spacer_2) * 2, peg_y + peg_size + spacer_2),
              'peg_pink' : (peg_x + (peg_size + spacer_2) * 3, peg_y + peg_size + spacer_2),
              'peg_active' : (peg_x, active_peg_y),
              'guess_peg_1' : (guess_peg_x, spacer_1),
              'guess_peg_2' : (guess_peg_x + peg_size + spacer_2, spacer_1),
              'guess_peg_3' : (guess_peg_x + (peg_size + spacer_2) * 2, spacer_1),
              'guess_peg_4' : (guess_peg_x + (peg_size + spacer_2) * 3, spacer_1),
              'guess_peg_5' : (guess_peg_x + (peg_size + spacer_2) * 4, spacer_1),
              'guess_peg_6' : (guess_peg_x + (peg_size + spacer_2) * 5, spacer_1),
              'scroll_up' : (scroll_x, spacer_1),
              'scroll_down' : (scroll_x, spacer_1 + s['scroll'][1] + spacer_2),
              'submit' : (guess_peg_x, spacer_1 + spacer_2 + peg_size),
              'prev_guess_peg_start' : (guess_peg_x, prev_guess_peg_y),
              'prev_guess_response_start' : (scroll_x, prev_guess_peg_y),
              'prev_guess_response2_start' : (scroll_x, prev_guess_peg_y + s['response'][1] + spacer_2),
              'div' : (div_x, -10),
              'turn_no_btn' : (turn_btn_x, turn_btn_y),
              'turn_btn_offset' : (0, peg_size / 4),
              'turn_text_offset' : (turn_offset_x, turn_offset_y),
              'response_text_offset' : (restxt_offset_x, restxt_offset_y)
             }
        self.control_positions_dict = p

        # Peg colours
        self.pegColours = { 'red' : wx.Colour(250, 130, 130),
                            'orange' : wx.Colour(250, 206, 105),
                            'yellow' : wx.Colour(255, 255, 158),
                            'green' : wx.Colour(199, 250, 105),
                            'blue' : wx.Colour(105, 207, 250),
                            'violet' : wx.Colour(105, 134, 250),
                            'purple' : wx.Colour(173, 105, 250),
                            'pink' : wx.Colour(251, 145, 255) }
                         
        # Styles
        self.UI_styles = [ 'default', 'unicorn', 'jungle' ]
        self.colours_dict = { 'light blue' : wx.Colour(217, 252, 251),
                              'lavender' : wx.Colour(231, 217, 252),
                              'pink' : wx.Colour(253, 201, 255),
                              'red' : wx.Colour(255, 20, 20),
                              'white' : wx.Colour(255, 255, 255),
                              'light yellow' : wx.Colour(252, 252, 217),
                              'blue' : wx.Colour(18, 77, 255),
                              'new_1' : wx.Colour(217, 252, 223),
                              'new_2' : wx.Colour(250, 252, 217),
                              'light grey' : wx.Colour(230, 230, 230),
                              'medium grey' : wx.Colour(190, 190, 190),
                              'dark grey' : wx.Colour(74, 73, 74) }

        self.UIcolour_background_dict = { 'default' : 'light grey',
                                          'beach' : 'light yellow', 
                                          'unicorn' : 'lavender',
                                          'circus' : 'white',
                                          'dark mode' : 'dark grey',
                                          'jungle' : 'new_1'
                                         }
        self.UIcolour_button_dict = { 'default' : 'medium grey',
                                      'beach' : 'light blue', 
                                      'unicorn' : 'light blue',
                                      'circus' : 'red',
                                      'dark mode' : 'light grey',
                                      'jungle' : 'light yellow'
                                     }
                                     
        self.UIcolour_nullButton_dict = { 'default' : 'white',
                                          'beach' : 'white',
                                          'unicorn' : 'white',
                                          'circus' : 'light grey',
                                          'dark mode' : 'white',
                                          'jungle' : 'white'
                                         }
                                         
    def InitUI(self):
        # Window settings
        self.WindowSize = (self.control_sizes_dict['frame_default'])
        self.SetSize(self.WindowSize)
        self.SetTitle('Mastermind')
        self.Centre()
        
        # Arrays for buttons/guesses/responses
        self.UI_buttons = []
        self.UI_nullButtons = []
        self.UI_dark = []
        self.prev_guesses = []
        self.prev_guess_buttons = []
        self.responses = []
        self.response_buttons = []
        self.response_text = []
        self.turn_buttons = []
        self.turn_text = []
        self.guess_buttons = []
        self.win_lose_btn_on = False

        # Colour palette
        self.ChangePalette('unicorn')
        
        # Initialize peg colour
        self.CurrentPegColour = self.colours[0]

    def ChangePalette(self, style):
        if style in self.UI_styles:
            self.CurrentPalette = style
            self.UIcolour_background = self.colours_dict[self.UIcolour_background_dict[style]]
            self.SetBackgroundColour(self.UIcolour_background)
            self.UIcolour_button = self.colours_dict[self.UIcolour_button_dict[style]]
            self.UIcolour_nullButton = self.colours_dict[self.UIcolour_nullButton_dict[style]]
            self.UIcolour_font = wx.BLACK
            self.current_guess = [''] * self.code_length
            for btn in self.UI_buttons:
                btn.SetBaseColours(startcolour=self.UIcolour_button, foregroundcolour=self.UIcolour_font)
            for btn in self.UI_nullButtons:
                btn.SetBaseColours(startcolour=self.UIcolour_nullButton, foregroundcolour=self.UIcolour_font)
    
    # ***************************************************************************************************
    # SET UP GAME SCREEN*********************************************************************************
    # ***************************************************************************************************

    def GameScreen_Create(self):
        # Initialize code
        self.Code = self.RandomizeCode()
        
        # Set up screen
        self.GameScreen_Create_MainControls()
        self.GameScreen_Create_ColourControls()
        self.GameScreen_Create_Settings()
        self.GameScreen_Create_Guesses()
        
    def GameScreen_Create_MainControls(self):
        # Get dictionaries
        s = self.control_sizes_dict
        p = self.control_positions_dict
        
        # New game button
        self.btn_newGame = UI_btn(self.pnl, 'New Game', p['btn_newgame'], s['btn_med'],
                                  self.NewGame, self.UIcolour_button, self.UIcolour_font)
        self.UI_buttons.append(self.btn_newGame)
        
        # Restart game button
        self.btn_restartGame = UI_btn(self.pnl, 'Restart Game', p['btn_restartgame'], s['btn_med'],
                                  self.RestartGame, self.UIcolour_button, self.UIcolour_font)
        self.UI_buttons.append(self.btn_restartGame)
        
        # Divider
        self.div = UI_btn(self.pnl, '', p['div'], s['div'], self.Inactive, self.UIcolour_button, disabled=True)
        self.UI_buttons.append(self.div)
        
        # Turn button
        self.GameScreen_Create_TurnButton()
        
    def GameScreen_Create_ColourControls(self):
        # Get dictionaries
        s = self.control_sizes_dict
        p = self.control_positions_dict
        
        # For each colour
        self.btn_red = UI_btn(self.pnl, '', p['peg_red'], s['peg'], self.Peg_Red, self.pegColours['red'])
        self.btn_orange = UI_btn(self.pnl, '', p['peg_orange'], s['peg'], self.Peg_Orange, self.pegColours['orange'])
        self.btn_yellow = UI_btn(self.pnl, '', p['peg_yellow'], s['peg'], self.Peg_Yellow, self.pegColours['yellow'])
        self.btn_green = UI_btn(self.pnl, '', p['peg_green'], s['peg'], self.Peg_Green, self.pegColours['green'])
        self.btn_blue = UI_btn(self.pnl, '', p['peg_blue'], s['peg'], self.Peg_Blue, self.pegColours['blue'])
        self.btn_violet = UI_btn(self.pnl, '', p['peg_violet'], s['peg'], self.Peg_Violet, self.pegColours['violet'])
        self.btn_purple = UI_btn(self.pnl, '', p['peg_purple'], s['peg'], self.Peg_Purple, self.pegColours['purple'])
        self.btn_pink = UI_btn(self.pnl, '', p['peg_pink'], s['peg'], self.Peg_Pink, self.pegColours['pink'])
        
        # Active colour button
        self.btn_active = UI_btn(self.pnl, '', p['peg_active'], s['peg_active'], self.Inactive, self.pegColours[self.CurrentPegColour.lower()], disabled=True)
        
    def GameScreen_Create_Settings(self):
        # Get dictionaries
        s = self.control_sizes_dict
        p = self.control_positions_dict
        
        # Add palette button and give up button
        self.btn_palette = UI_btn(self.pnl, 'Change Palette', p['palette'], s['btn_sml'], 
                                  self.NextPalette, self.UIcolour_button, self.UIcolour_font)
        self.UI_buttons.append(self.btn_palette)
        self.btn_giveup = UI_btn(self.pnl, 'Give Up', p['give_up'], s['btn_sml'],
                                 self.GiveUp, self.UIcolour_button, self.UIcolour_font)
        self.UI_buttons.append(self.btn_giveup)
        
        # Add code length button and label
        self.btn_codelength_1 = UI_btn(self.pnl, 'Code length', p['code_length'], s['btn_sml'], 
                                       self.ChangeCodeLength, self.UIcolour_button)
        self.btn_codelength_2 = UI_btn(self.pnl, '', p['code_length_2'], s['btn_option'], 
                                       self.Inactive, self.UIcolour_nullButton)
        self.txt_codelength = wx.StaticText(self.pnl, label=str(self.code_length),
                                            pos=(p['code_length_2'][0] + p['code_length_text_offset'][0], 
                                                 p['code_length_2'][1] + p['code_length_text_offset'][1]))
        self.UI_buttons.append(self.btn_codelength_1)
        self.UI_nullButtons.append(self.btn_codelength_2)
        
        # Add multiples button and label
        self.btn_multi = UI_btn(self.pnl, 'Multiples allowed', p['multis'], s['btn_sml'], 
                                self.MultiplesOnOff, self.UIcolour_button)
        self.btn_multi_2 = UI_btn(self.pnl, '', p['multis_2'], s['btn_option'],
                                  self.Inactive, self.UIcolour_nullButton)
        self.txt_multi = wx.StaticText(self.pnl, label=self.multiples,
                                       pos=(p['multis_2'][0] + p['multis_text_offset'][0],
                                            p['multis_2'][1] + p['multis_text_offset'][1]))
        self.UI_buttons.append(self.btn_multi)
        self.UI_nullButtons.append(self.btn_multi_2)
        
    def GameScreen_Create_Guesses(self):
        # Get dictionaries
        s = self.control_sizes_dict
        p = self.control_positions_dict
        
        # Submit button
        self.btn_submit = UI_btn(self.pnl, 'Submit Guess', p['submit'], s['submit'], 
                                 self.SubmitGuess, self.UIcolour_button, self.UIcolour_font)
        self.UI_buttons.append(self.btn_submit)
        
        # Current guess buttons
        self.btn_guess1 = UI_btn(self.pnl, '', p['guess_peg_1'], s['peg'], self.Guess1, wx.WHITE)
        self.btn_guess2 = UI_btn(self.pnl, '', p['guess_peg_2'], s['peg'], self.Guess2, wx.WHITE)
        self.btn_guess3 = UI_btn(self.pnl, '', p['guess_peg_3'], s['peg'], self.Guess3, wx.WHITE)
        self.guess_buttons.append(self.btn_guess1)
        self.guess_buttons.append(self.btn_guess2)
        self.guess_buttons.append(self.btn_guess3)
        self.GameScreen_CreateAdditionalGuesses()
        
    def GameScreen_CreateAdditionalGuesses(self):
        # Get dictionaries
        s = self.control_sizes_dict
        p = self.control_positions_dict
        
        # If buttons do not exist, create as required
        if self.code_length >= 4 and len(self.guess_buttons) < 4:
            self.btn_guess4 = UI_btn(self.pnl, '', p['guess_peg_4'], s['peg'], self.Guess4, wx.WHITE)
            self.guess_buttons.append(self.btn_guess4)
        if self.code_length >= 5 and len(self.guess_buttons) < 5:
            self.btn_guess5 = UI_btn(self.pnl, '', p['guess_peg_5'], s['peg'], self.Guess5, wx.WHITE)
            self.guess_buttons.append(self.btn_guess5)
        if self.code_length >= 6 and len(self.guess_buttons) < 6:
            self.btn_guess6 = UI_btn(self.pnl, '', p['guess_peg_6'], s['peg'], self.Guess6, wx.WHITE)
            self.guess_buttons.append(self.btn_guess6)
        
        # Reset guess
        self.current_guess = [''] * self.code_length

    def AdjustSubmitButton(self, create_new=False, null_button=False, new_label='Submit Guess'):
        # Get dictionaries
        s = self.control_sizes_dict
        p = self.control_positions_dict
        
        # Get index in array and destroy old submit button
        self.UI_buttons.remove(self.btn_submit)
        self.btn_submit.Destroy()
        
        # Create new submit button if specified
        if create_new:
            if null_button:
                btn_colour = self.UIcolour_nullButton
            else:
                btn_colour = self.UIcolour_button
            self.btn_submit = UI_btn(self.pnl, new_label, p['submit'], s['submit'], 
                                     self.SubmitGuess, btn_colour, self.UIcolour_font)
            self.UI_buttons.append(self.btn_submit)
            
            if null_button:
                self.btn_submit.Enable(False)
                self.UI_nullButtons.append(self.btn_submit)
            else:
                self.UI_buttons.append(self.btn_submit)
            

        # Get index in array and destroy old turn button
        self.UI_buttons.remove(self.turn_button)
        self.turn_button.Destroy()
        self.turn_txt_current.Destroy()
        
        # Create new turn button and add to array
        self.GameScreen_Create_TurnButton()
        
    # ***************************************************************************************************
    # SCROLL BUTTONS*************************************************************************************
    # ***************************************************************************************************
        
    def AdjustScrollButtons(self, up=True, down=True):
        if self.scroll_index == len(self.prev_guesses) - self.max_guesses_displayed:
            self.scroll_up.SetBaseColours(startcolour=self.UIcolour_nullButton)
        else:
            self.scroll_up.SetBaseColours(startcolour=self.UIcolour_button, foregroundcolour=self.UIcolour_font)
        if self.scroll_index == 0:
            self.scroll_down.SetBaseColours(startcolour=self.UIcolour_nullButton)
        else:
            self.scroll_down.SetBaseColours(startcolour=self.UIcolour_button, foregroundcolour=self.UIcolour_font)
                
    def ScrollUp(self, event):
        if self.scroll_index < len(self.prev_guesses) - self.max_guesses_displayed:
            self.scroll_index = self.scroll_index + 1
            self.DisplayGuesses()
            self.DisplayResponses()
            self.DisplayTurns()
            self.AdjustScrollButtons()
        
    def ScrollDown(self, event):
        if self.scroll_index != 0:
            self.scroll_index = self.scroll_index - 1
            self.DisplayGuesses()
            self.DisplayResponses()
            self.DisplayTurns()
            self.AdjustScrollButtons()
    
    # ***************************************************************************************************
    # PREVIOUS GUESSES/RESPONSES*************************************************************************
    # ***************************************************************************************************
    
    def DisplayGuesses(self):
        # If required, get subset of guesses for display
        if len(self.prev_guesses) > self.max_guesses_displayed:
            guesses = self.prev_guesses[self.scroll_index:self.max_guesses_displayed + self.scroll_index]
        else:
            guesses = self.prev_guesses
        
        # Check that number of guess colours is the same as the number of buttons
        assert(len(guesses)==len(self.prev_guess_buttons))
        assert(len(guesses[0])==len(self.prev_guess_buttons[0]))
        
        # Re-colour buttons for guesses
        for i in range(0, len(self.prev_guess_buttons)):
            for j in range(0, len(self.prev_guess_buttons[i])):
                colour = guesses[len(guesses) - i - 1][j]
                self.prev_guess_buttons[i][j].SetBaseColours(startcolour=self.pegColours[colour])
    
    def DisplayResponses(self):
        # If required, get subset of responses for display
        if len(self.responses) > self.max_guesses_displayed:
            res = self.responses[self.scroll_index:self.max_guesses_displayed + self.scroll_index]
        else:
            res = self.responses
            
        # Check that number of responses is the same as number of buttons
        assert(len(res) == len(self.response_buttons))
        
        # Change response texts
        for i in range(0, len(res)):
            for j in [0, 1]:
                self.response_buttons[len(res) - i - 1][j].SetLabel(str(res[i][j]))
            
    # ***************************************************************************************************
    # TURN BUTTONS***************************************************************************************
    # ***************************************************************************************************
        
    def DisplayTurns(self):
        # Change turn texts
        for i in range(0, len(self.turn_text)):
            this_turn_text = ('Turn ' + str(len(self.turn_text) - i + self.scroll_index)).rjust(7, ' ').rjust(8, ' ')
            self.turn_text[i].SetLabel(this_turn_text)
    
    def ResetTurns(self):
        self.this_turn = 1
        self.turn_txt_current.SetLabel(('Turn ' + str(self.this_turn)).rjust(7, ' ').rjust(8, ' '))
        
    def GameScreen_Create_TurnButton(self):
        # Get dictionaries
        s = self.control_sizes_dict
        p = self.control_positions_dict
        
        # Turn button
        turn_btn_x = p['turn_no_btn'][0]
        turn_btn_y = p['guess_peg_1'][1] + self.control_positions_dict['turn_btn_offset'][1]
        turn_text_x = turn_btn_x + p['turn_text_offset'][0]
        turn_text_y = turn_btn_y + p['turn_text_offset'][1]
        self.turn_button = UI_btn(self.pnl, '', (turn_btn_x, turn_btn_y), 
                                  s['turn'], self.Inactive, self.UIcolour_button, disabled=True)
        self.turn_txt_current = wx.StaticText(self.pnl, -1, ('Turn ' + str(self.this_turn)).rjust(7, ' ').rjust(8, ' '), 
                                              pos=(turn_text_x, turn_text_y))
        self.UI_buttons.append(self.turn_button)
        
    # ***************************************************************************************************
    # LEFT PANEL BUTTONS*********************************************************************************
    # ***************************************************************************************************
        
    def NewGame(self, event):
        self.ClearGameScreen()
        self.AdjustSubmitButton(create_new=True)
        self.Code = self.RandomizeCode()
        self.EnableGuesses()
        self.ResetTurns()
        
    def RestartGame(self, event):
        self.ClearGameScreen()
        self.AdjustSubmitButton(create_new=True)
        self.EnableGuesses()
        self.ResetTurns()
        
    def ChangeCodeLength(self, event):
        # Adjust button and text
        self.code_length = self.code_length + 1
        if self.code_length > self.max_code_length : self.code_length = self.min_code_length
        self.txt_codelength.SetLabel(str(self.code_length))
        
        # Reset positioning based on additional buttons
        self.ReferenceDicts()
        
        # Restart game and get new code
        self.ClearGameScreen()
        self.ResetTurns()
        self.Code = self.RandomizeCode()
        
        # Add or remove guess buttons
        if self.code_length == self.min_code_length:
            self.GameScreen_Delete_Guesses()
            self.GameScreen_Create_Guesses()
        else:
            self.GameScreen_Delete_Guesses()
            self.GameScreen_Create_Guesses()
    
    def MultiplesOnOff(self, event):
        if self.multiples == 'Off':
            self.multiples = 'On'
            self.max_instance_of_each_colour = 1
        elif self.multiples == 'On':
            self.multiples = 'Off'
            self.max_instance_of_each_colour = self.code_length
        self.txt_multi.SetLabel(self.multiples)
        
        # Restart game and get new code
        self.ClearGameScreen()
        self.ResetTurns()
        self.Code = self.RandomizeCode()
        
    def NextPalette(self, event):
        self.ChangePalette(self.UI_styles[self.UI_styles.index(self.CurrentPalette) - 1])
    
    def GiveUp(self, event):
        # Make submit button null colour, disable, and change text to 'ANSWER'
        self.AdjustSubmitButton(create_new=True, null_button=True, new_label='ANSWER')
        
        # Disable guess buttons
        self.DisableGuesses()
        
        # Add answer to guess buttons
        for i in range(0, len(self.Code)):
            self.guess_buttons[i].SetBaseColours(startcolour=self.pegColours[self.Code[i]])
    
    # ***************************************************************************************************
    # SUBMIT GUESS***************************************************************************************
    # ***************************************************************************************************
    
    def SubmitGuess(self, event):
        # Only accept guess if all positions filled
        if '' not in self.current_guess:
            # If guess won, run win function
            if self.current_guess == self.Code:
                self.GameWin()
            # If game lost, run loss function
            elif self.this_turn == self.max_guesses:
                self.GameLoss()
            # Otherwise, add guess to previous guesses
            else:
                self.AddNewGuess()
    
    def AddNewGuess(self):
        # Get size/position references
        increment = self.peg_size + self.spacer_2
        pos_x_start = self.control_positions_dict['prev_guess_peg_start'][0]
        pos_y = self.control_positions_dict['prev_guess_peg_start'][1] + increment * (len(self.prev_guesses) - 1)
        peg_size = self.control_sizes_dict['peg']
        pos_scroll_up = self.control_positions_dict['scroll_up']
        pos_scroll_down = self.control_positions_dict['scroll_down']
        scroll_size = self.control_sizes_dict['scroll']
        pos_res_x = self.control_positions_dict['prev_guess_response_start'][0]
        pos_res1_y = self.control_positions_dict['prev_guess_response_start'][1] + increment * (len(self.prev_guesses) - 1) 
        pos_res2_y = self.control_positions_dict['prev_guess_response2_start'][1] + increment * (len(self.prev_guesses) - 1)
        size_res = self.control_sizes_dict['response']
        text_offset_x = size_res[0]/3.3
        text_offset_y = size_res[1]/6.5
        turn_btn_x = self.control_positions_dict['turn_no_btn'][0]
        turn_btn_offset_y = self.control_positions_dict['turn_btn_offset'][1]
        turn_size = self.control_sizes_dict['turn']
        turn_text_offset_x = self.control_positions_dict['turn_text_offset'][0]
        turn_text_offset_y = self.control_positions_dict['turn_text_offset'][1]

        # Add current guess to guesses
        self.prev_guesses.append(self.current_guess)
        
        # Add current response to responses
        self.responses.append(self.GetMasterResponse())
        
        # If required, add an extra row of buttons to display an additional guess
        if len(self.prev_guesses) <= self.max_guesses_displayed:
            
            # Add buttons to display additional guess
            new_buttons = []
            for i in range(0, len(self.current_guess)):
                new_btn = prev_guess_btn(self.pnl, (pos_x_start + increment * i, pos_y), peg_size)
                new_buttons.append(new_btn)
            self.prev_guess_buttons.append(new_buttons)
            
            # Add buttons to display additional response
            res_1 = UI_btn(self.pnl, '', (pos_res_x, pos_res1_y), size_res, self.Inactive, self.UIcolour_button, disabled=True)
            res_2 = UI_btn(self.pnl, '', (pos_res_x, pos_res2_y), size_res, self.Inactive, self.UIcolour_nullButton, disabled=True)
            self.response_buttons.append([res_1, res_2])
            
            # Add text to response buttons
            text_1 = wx.StaticText(self.pnl, -1, label='', pos=(pos_res_x + text_offset_x, pos_res1_y + text_offset_y))
            text_2 = wx.StaticText(self.pnl, -1, label='', pos=(pos_res_x + text_offset_x, pos_res2_y + text_offset_y))
            self.response_text.append(text_1)
            self.response_text.append(text_2)
            
            # Add turn button and text
            turn_btn = UI_btn(self.pnl, '', (turn_btn_x, pos_res1_y + turn_btn_offset_y), turn_size, self.Inactive, self.UIcolour_nullButton, disabled=True)
            turn_txt = wx.StaticText(self.pnl, -1, label='', pos=(turn_btn_x + turn_text_offset_x, pos_res1_y + turn_btn_offset_y + turn_text_offset_y))
            self.turn_buttons.append(turn_btn)
            self.turn_text.append(turn_txt)
            
        # If guess is more than can fit into UI, add scroll buttons
        elif len(self.prev_guesses) == self.max_guesses_displayed + 1:
            self.scroll_up = UI_btn(self.pnl, '\u2191', pos_scroll_up, scroll_size, 
                                    self.ScrollUp, self.UIcolour_button, self.UIcolour_font)
            self.scroll_down = UI_btn(self.pnl, '\u2193', pos_scroll_down, scroll_size, 
                                          self.ScrollDown, self.UIcolour_button, self.UIcolour_font)
            self.scroll_on = True
            self.UI_buttons.append(self.scroll_up)
            self.UI_buttons.append(self.scroll_down)
            
        # If required, reset scroll index and buttons
        if len(self.prev_guesses) > self.max_guesses_displayed:
            self.scroll_index = len(self.prev_guesses) - self.max_guesses_displayed
            self.AdjustScrollButtons()
            
        # Display guesses/responses/turn numbers
        self.DisplayGuesses()
        self.DisplayResponses()
        self.DisplayTurns()
        
        # Increment turn
        self.this_turn = self.this_turn + 1
        self.turn_txt_current.SetLabel(('Turn ' + str(self.this_turn)).rjust(7, ' ').rjust(8, ' '))
        
        # Reset
        self.ClearGameScreen(clearGuessOnly=True)
        self.current_guess = [''] * self.code_length
    
    # ***************************************************************************************************
    # COLOUR PEGS****************************************************************************************
    # ***************************************************************************************************
    
    def ChangeActiveColour(self, colour):
        self.CurrentPegColour = colour
        self.btn_active.SetBaseColours(startcolour=self.pegColours[colour])
    
    def Peg_Red(self, event):
        self.ChangeActiveColour('red')
        
    def Peg_Orange(self, event):
        self.ChangeActiveColour('orange')
        
    def Peg_Yellow(self, event):
        self.ChangeActiveColour('yellow')
        
    def Peg_Green(self, event):
        self.ChangeActiveColour('green')
        
    def Peg_Blue(self, event):
        self.ChangeActiveColour('blue')
        
    def Peg_Violet(self, event):
        self.ChangeActiveColour('violet')
        
    def Peg_Purple(self, event):
        self.ChangeActiveColour('purple')
        
    def Peg_Pink(self, event):
        self.ChangeActiveColour('pink')
    
    # ***************************************************************************************************
    # GUESS BUTTONS**************************************************************************************
    # ***************************************************************************************************
    
    def EnableGuesses(self):
        for btn in self.guess_buttons : btn.Enable(True)
        
    def DisableGuesses(self):
        for btn in self.guess_buttons : btn.Enable(False)
                
    def Inactive(self, event):
        pass
    
    def Guess1(self, event):
        if self.current_guess[0]!=self.CurrentPegColour:
            self.btn_guess1.SetBaseColours(startcolour=self.pegColours[self.CurrentPegColour])
            self.current_guess[0] = self.CurrentPegColour
        else:
            self.btn_guess1.SetBaseColours(startcolour=wx.WHITE)
            self.current_guess[0] = ''
        
    def Guess2(self, event):
        if self.current_guess[1]!=self.CurrentPegColour:
            self.btn_guess2.SetBaseColours(startcolour=self.pegColours[self.CurrentPegColour])
            self.current_guess[1] = self.CurrentPegColour
        else:
            self.btn_guess2.SetBaseColours(startcolour=wx.WHITE)
            self.current_guess[1] = ''
        
    def Guess3(self, event):
        if self.current_guess[2]!=self.CurrentPegColour:
            self.btn_guess3.SetBaseColours(startcolour=self.pegColours[self.CurrentPegColour])
            self.current_guess[2] = self.CurrentPegColour
        else:
            self.btn_guess3.SetBaseColours(startcolour=wx.WHITE)
            self.current_guess[2] = ''
        
    def Guess4(self, event):
        if self.current_guess[3]!=self.CurrentPegColour:
            self.btn_guess4.SetBaseColours(startcolour=self.pegColours[self.CurrentPegColour])
            self.current_guess[3] = self.CurrentPegColour
        else:
            self.btn_guess4.SetBaseColours(startcolour=wx.WHITE)
            self.current_guess[3] = ''
    
    def Guess5(self, event):
        if self.current_guess[4]!=self.CurrentPegColour:
            self.btn_guess5.SetBaseColours(startcolour=self.pegColours[self.CurrentPegColour])
            self.current_guess[4] = self.CurrentPegColour
        else:
            self.btn_guess5.SetBaseColours(startcolour=wx.WHITE)
            self.current_guess[4] = ''
            
    def Guess6(self, event):
        if self.current_guess[5]!=self.CurrentPegColour:
            self.btn_guess6.SetBaseColours(startcolour=self.pegColours[self.CurrentPegColour])
            self.current_guess[5] = self.CurrentPegColour
        else:
            self.btn_guess6.SetBaseColours(startcolour=wx.WHITE)
            self.current_guess[5] = ''
    
    # ***************************************************************************************************
    # GAME BACK END**************************************************************************************
    # ***************************************************************************************************
    
    def RandomizeCode(self):
    # Loop until valid code found and returned
    # (Other methods may weight multiples to being early on in the code)
        seed_val = random.randint(0, len(self.colours) ** self.code_length)
        random.seed(seed_val)
        while True:
            # Generate code
            code = [""] * self.code_length
            for i in range(0, self.code_length):
                code[i] = self.colours[random.randint(0, len(self.colours) - 1)]
            
            # Check validity
            valid = True
            for i in range(0, self.code_length):
                if code.count(code[i]) > self.max_instance_of_each_colour : valid = False
            if valid : return code
            
    def GetMasterResponse(self):
        # For a guess code, checks against a master code and returns
        # a vector [a, b] where a is the number of correct letters and 
        # positions and b is the number of correct letters
        a = 0
        b = 0
        for i in range(0, len(self.current_guess)):
            if self.current_guess[i] == self.Code[i]:
                a = a + 1
        for i in range(0, len(self.Code)):
            if self.Code[i] in self.current_guess:
                b = b + 1
        b = max([b - a, 0])
        return ([a, b])
    
    # ***************************************************************************************************
    # WIN/LOSE*******************************************************************************************
    # ***************************************************************************************************
    
    def GameWin(self):
        self.DisableGuesses()
        self.btn_winlose = UI_btn(self.pnl, 'GAME WON ON TURN ' + str(self.this_turn),
                                  self.control_positions_dict['submit'], self.control_sizes_dict['submit'], 
                                  self.SubmitGuess, self.UIcolour_nullButton, self.UIcolour_font)
        self.win_lose_btn_on = True
        
    def GameLoss(self):
        self.DisableGuesses()
        self.btn_winlose = UI_btn(self.pnl, 'GAME LOST - OUT OF TURNS',
                                  self.control_positions_dict['submit'], self.control_sizes_dict['submit'], 
                                  self.SubmitGuess, self.UIcolour_nullButton, self.UIcolour_font)
        self.win_lose_btn_on = True
        
    # ***************************************************************************************************
    # CLEAR SCREEN***************************************************************************************
    # ***************************************************************************************************
        
    def ClearGameScreen(self, clearGuessOnly=False):
        # Reset colours on guess buttons
        for btn in self.guess_buttons : btn.SetBaseColours(startcolour=wx.WHITE)
        
        if not clearGuessOnly:
            # Remove previous guess buttons
            for guess_row in self.prev_guess_buttons:
                for btn in guess_row:
                    btn.Destroy()
                    
            # Remove response buttons/responses
            for response_set in self.response_buttons:
                for btn in response_set:
                    btn.Destroy()
            for txt in self.response_text : txt.Destroy()
            
            # Remove turn buttons and text
            for txt in self.turn_text : txt.Destroy()
            for btn in self.turn_buttons : btn.Destroy()
            
            # Remove win/lose button
            if self.win_lose_btn_on:
                self.btn_winlose.Destroy()
                self.win_lose_btn_on = False

            # Remove scroll buttons
            if self.scroll_on:
                self.UI_buttons.remove(self.scroll_up)
                self.UI_buttons.remove(self.scroll_down)
                self.scroll_up.Destroy()
                self.scroll_down.Destroy()
                self.scroll_on = False
                
            # Reset variable arrays
            self.prev_guess_buttons = []
            self.prev_guesses = []
            self.responses = []
            self.response_buttons = []
            self.response_text = []
            self.turn_text = []
            self.turn_buttons = []

    def GameScreen_Delete_Guesses(self):
        # Delete guess buttons
        for btn in self.guess_buttons : btn.Destroy()
        self.guess_buttons = []
        
        # Resize submit button
        self.AdjustSubmitButton()
        
        # Reset guess
        self.current_guess = [''] * self.code_length

    # ***************************************************************************************************
    # ***************************************************************************************************
    # ***************************************************************************************************
        
# *******************************************************************************************************
# BUTTON CLASSES*****************************************************************************************
# *******************************************************************************************************
        
class prev_guess_btn(gb.GradientButton):
    def __init__(self, parent, pos, size, btn_colour=wx.WHITE):
        gb.GradientButton.__init__(self, parent, pos=pos, size=size)
        self.SetBaseColours(startcolour=btn_colour)
        self.Enable(False)
        
    def NewColour(self, colour):
        self.SetBaseColours(startcolour=self.colours(colour))
    
class UI_btn(gb.GradientButton):
    def __init__(self, parent, label, pos, size, fn, btn_colour=wx.WHITE, font_colour=wx.BLACK, disabled=False):
        gb.GradientButton.__init__(self, parent, label=label, pos=pos, size=size)
        self.SetBaseColours(startcolour=btn_colour, foregroundcolour=font_colour)
        self.Bind(wx.EVT_BUTTON, fn)
        if disabled : self.Enable(False)
        
# *******************************************************************************************************
# MAIN***************************************************************************************************
# *******************************************************************************************************
        
# Create app
app = wx.App()

# Display frame
frm = UI(None)
frm.Show()
frm.Centre()
app.MainLoop()
    
