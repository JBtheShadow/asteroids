require "globals"
local love = require "love"

function Asteroid(x, y, params)
    local size = params and params.size or ASTEROID_SIZE
    local level = params and params.level or 1

    local ASTEROID_MIN_SIZE = 35
    local ASTEROID_COUNT = 3
    local ASTEROID_VERT = 10
    local ASTEROID_JAG = 0.4
    local ASTEROID_SPEED = math.random(50) + level * 2

    local vert = math.floor(math.random(ASTEROID_VERT + 1) + ASTEROID_VERT / 2)
    local offset = {}
    for i = 1, vert + 1 do
        table.insert(offset, ASTEROID_JAG * (2 * math.random() - 1) + 1)
    end

    local sign = function()
        return math.random() < 0.5 and 1 or -1
    end

    return {
        x = x,
        y = y,
        x_vel = math.random() * ASTEROID_SPEED * sign(),
        y_vel = math.random() * ASTEROID_SPEED * sign(),
        size = size,
        radius = math.ceil(size / 2),
        angle = math.rad(math.random(math.pi)),
        vert = vert,
        offset = offset,

        draw = function(self, faded)
            local opacity = faded and 0.5 or 1

            local _x, _y, r, o, a = self.x, self.y, self.radius, self.offset, self.angle
            local sin, cos, pi = math.sin, math.cos, math.pi
            local points = { (_x + r * o[1] * cos(a)), (_y + r * o[1] * sin(a)) }
            for i = 1, self.vert - 1 do
                table.insert(points, _x + r * o[i + 1] * cos(a + i * pi * 2 / self.vert))
                table.insert(points, _y + r * o[i + 1] * sin(a + i * pi * 2 / self.vert))
            end

            love.graphics.setColor(0.7, 0.7, 0.7, opacity)
            love.graphics.polygon("line", points)

            if show_debugging then
                love.graphics.setColor(1, 0, 0, opacity)
                love.graphics.circle("fill", self.x, self.y, 1) --center
                love.graphics.circle("line", self.x, self.y, self.radius) --hitbox
            end
        end,

        move = function(self, dt)
            self.x = self.x + self.x_vel * dt
            self.y = self.y + self.y_vel * dt

            if self.x + self.radius < 0 then
                self.x = love.graphics.getWidth() + self.radius
            elseif self.x - self.radius > love.graphics.getWidth() then
                self.x = -self.radius
            end

            if self.y + self.radius < 0 then
                self.y = love.graphics.getHeight() + self.radius
            elseif self.y - self.radius > love.graphics.getHeight() then
                self.y = -self.radius
            end
        end,

        destroy = function(self, asteroids_tbl, index, game)
            table.remove(asteroids_tbl, index)

            local newSize = self.size * 0.6
            if newSize > ASTEROID_MIN_SIZE then
                local count = math.random(2, ASTEROID_COUNT)
                for i = 1, count do
                    table.insert(asteroids_tbl, 1, Asteroid(self.x, self.y, { size = newSize + math.random(10), level = self.level }))
                end
            end
        end,
    }
end

return Asteroid