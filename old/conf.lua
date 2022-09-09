local love = require "love"

function love.conf(t)
    t.console = true
    t.window.title = "Asteroids"
    t.window.width = 1280
    t.window.height = 720
end