local love = require "love"
local Text = require "components.Text"
local Asteroid = require "objects.Asteroid"

function Game()
    return {
        level = 1,
        state = {
            menu = true,
            paused = false,
            running = false,
            ended = false
        },

        changeGameState = function(self, state)
            self.state.menu = state == "menu"
            self.state.paused = state == "paused"
            self.state.running = state == "running"
            self.state.ended = state == "ended"
        end,

        draw = function(self, faded)
            if faded then

                -- love.graphics.setColor(0, 0, 0, 0.5)
                -- love.graphics.rectangle("fill", 0, 0, love.graphics.getWidth(), love.graphics.getHeight())

                Text("PAUSED", 0, love.graphics.getHeight() * 0.4, { font_size = "h1", align = "center"} ):draw()
            end
        end,

        startNewGame = function(self, player)
            self:changeGameState("running")

            _G.asteroids = {}

            local as_x = math.floor(math.random(love.graphics.getWidth()))
            local as_y = math.floor(math.random(love.graphics.getHeight()))

            table.insert(asteroids, 1, Asteroid(as_x, as_y, { level = self.level }))
        end,
    }
end

return Game