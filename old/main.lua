--[[===============================
    Asteroids
    01: Game Setup
    02: The Player
    03: The Thruster
    04: The Game State
    05: Game Text
    06: Asteroids
    07: Lasers
    08: Laser Collision Detection
    09: Player Collision Detection
    10: Player Lives
    11: The Menu
    12: Installing & Running LuaRocks
    13: The Score System
=================================]]

require "globals"
local love = require "love"
--require "lunajson"

local Player = require "objects.Player"
local Game = require "states.Game"
local Menu = require "states.Menu"

math.randomseed(os.time())

function love.load()
    love.mouse.setVisible(false)
    _G.mouse_x, _G.mouse_y = 0, 0
    _G.player = Player()
    _G.game = Game()
    --game:startNewGame(player)
    _G.menu = Menu(game, player)
end

function love.mousepressed(x, y, button, is_touch, presses)
    if button == 1 then
        if game.state.running then
            player:shoot()
        elseif game.state.menu then
            menu:click(x, y, 10)
        else
            _G.clicked = true
        end
    end
end

function love.keypressed(key)
    if game.state.running then
        if key == "w" or key == "up" or key == "kp8" then
            player.thrusting = true
        end

        if key == "space" or key == "down" or key == "s" or key == "kp5" then
            player:shoot()
        end

        if key == "escape" then
            player.thrusting = false
            game:changeGameState("paused")
        end
    elseif game.state.paused then
        if key == "escape" then
            game:changeGameState("running")
        end
    end
end

function love.keyreleased(key)
    if key == "w" or key == "up" or key == "kp8" then
        player.thrusting = false
    end
end

function love.update(dt)
    _G.mouse_x, _G.mouse_y = love.mouse.getPosition()
    if game.state.running then
        player:move(dt)

        for a_index, asteroid in pairs(asteroids) do

            local a_destroyed = false

            if not player:isExploding() then
                if getDistance(asteroid.x, asteroid.y, player.x, player.y) <= player.radius + asteroid.radius then
                    player:explode()

                    if player.lives > 1 and not a_destroyed then
                        asteroid:destroy(asteroids, a_index, game)
                        a_destroyed = true
                    end
                end
            end

            for _, laser in pairs(player.lasers) do
                if getDistance(asteroid.x, asteroid.y, laser.x, laser.y) <= asteroid.radius then
                    laser:explode()
                    if not player:isExploding() and not a_destroyed then
                        asteroid:destroy(asteroids, a_index, game)
                        a_destroyed = true
                    end
                end
            end

            if not a_destroyed then
                asteroid:move(dt)
            end
        end
    elseif game.state.menu then
        _G.clicked = false
    end
end

function love.draw()
    if game.state.running or game.state.paused then
        player:drawLives(game.state.paused)
        player:draw(game.state.paused)

        for _, asteroid in pairs(asteroids) do
            asteroid:draw(game.state.paused)
        end

        game:draw(game.state.paused)
    elseif game.state.menu then
        menu:draw(mouse_x, mouse_y, 10)
    end

    love.graphics.setColor(1, 1, 1, 1)

    if not game.state.running then
        love.graphics.circle("fill", mouse_x, mouse_y, 10)
    end

    if show_fps then
        love.graphics.print(love.timer.getFPS() .. " FPS", 10, 10)
    end
end