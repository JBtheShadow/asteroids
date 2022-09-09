local love = require "love"

function Laser(x, y, angle)
    local LASER_SPEED = 500
    local LASER_SIZE = 3
    local EXPLODE_DUR = 0.1

    local statusEnum = {
        fired = 0,
        exploding = 1,
        done_exploding = 2,
    }

    return {
        x = x,
        y = y,
        x_vel = LASER_SPEED * math.cos(angle),
        y_vel = -LASER_SPEED * math.sin(angle),
        travel_time = 0,
        status = statusEnum.fired,
        explode_time = 0,

        hasExploded = function(self)
            return self.status == statusEnum.done_exploding or self.status == statusEnum.exploding
        end,

        doneExploding = function(self)
            return self.status == statusEnum.done_exploding
        end,

        draw = function(self, faded)
            local opacity = faded and 0.5 or 1

            if self.status == statusEnum.fired then
                love.graphics.setColor(1, 0.8, 0.1, opacity)
                love.graphics.setPointSize(LASER_SIZE)
                love.graphics.points(self.x, self.y)
            elseif self.status == statusEnum.exploding then
                love.graphics.setColor(1, 0.5, 0.2, opacity)
                love.graphics.circle("fill", self.x, self.y, 5)
                love.graphics.setColor(1, 0.9, 0.2, opacity)
                love.graphics.circle("fill", self.x, self.y, 2)
            end
        end,

        move = function(self, dt)
            if self.status == statusEnum.exploding then
                self.explode_time = self.explode_time + dt

                if self.explode_time > EXPLODE_DUR then
                    self.status = statusEnum.done_exploding
                    self.explode_time = 0
                end

                return
            end

            self.x = self.x + self.x_vel * dt
            self.y = self.y + self.y_vel * dt

            if self.x < 0 then
                self.x = love.graphics.getWidth()
            elseif self.x > love.graphics.getWidth() then
                self.x = 0
            end

            if self.y < 0 then
                self.y = love.graphics.getHeight()
            elseif self.y > love.graphics.getHeight() then
                self.y = 0
            end

            self.travel_time = self.travel_time + dt
        end,

        explode = function(self)
            self.status = statusEnum.exploding
        end,
    }
end

return Laser