local love = require "love"
local Button = require "components.Button"

function Menu(game, player)
    local funcs = {
        newGame = function()
            game:startNewGame(player)
        end,
        quitGame = function()
            love.event.quit()
        end,
    }

    local buttons = {
        Button(
            "New Game",
            love.graphics.getWidth() / 3,
            love.graphics.getHeight() * 0.25,
            {
                func = funcs.newGame,
                width = love.graphics.getWidth() / 3,
                height = 50,
                text_align = "center",
                font_size = "h3",
            }
        ),
        Button(
            "Settings",
            love.graphics.getWidth() / 3,
            love.graphics.getHeight() * 0.4,
            {
                func = nil,
                width = love.graphics.getWidth() / 3,
                height = 50,
                text_align = "center",
                font_size = "h3",
            }
        ),
        Button(
            "Quit",
            love.graphics.getWidth() / 3,
            love.graphics.getHeight() * 0.55,
            {
                func = funcs.quitGame,
                width = love.graphics.getWidth() / 3,
                height = 50,
                text_align = "center",
                font_size = "h3",
            }
        ),
    }

    return {
        draw = function(self, mouse_x, mouse_y, cursor_radius)
            for _, button in pairs(buttons) do
                button:draw(mouse_x, mouse_y, cursor_radius)
            end
        end,

        click = function(self, mouse_x, mouse_y, cursor_radius)
            for _, button in pairs(buttons) do
                if button:checkHover(mouse_x, mouse_y, cursor_radius) then
                    button:click()
                    break
                end
            end
        end,
    }
end

return Menu