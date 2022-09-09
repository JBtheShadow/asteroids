ASTEROID_SIZE = 100

_G.show_debugging = false
_G.show_fps = true
--_G.destroy_asteroid = false

function _G.getDistance(x1, y1, x2, y2)
    return math.sqrt((x2 - x1)^2 + (y2 - y1)^2)
end