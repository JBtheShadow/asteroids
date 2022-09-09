require "globals"
local love = require "love"

local Laser = require "objects.Laser"

function Player(lives)
    local SHIP_SIZE = 30
    local EXPLODE_DUR = 1
    local VIEW_ANGLE = math.rad(90)
    local LASER_LIMIT = 3
    local LASER_TIMER = 1.5
    local STARTING_LIVES = 3

    local statusEnum = {
        alive = 0,
        exploding = 1,
    }

    return {
        x = love.graphics.getWidth() / 2,
        y = love.graphics.getHeight() / 2,
        radius = SHIP_SIZE / 2,
        angle = VIEW_ANGLE,
        rotation = 0,
        lasers = {},
        thrusting = false,
        thrust = {
            x = 0,
            y = 0,
            speed = 5,
            big_flame = false,
            flame = 2.0
        },
        status = statusEnum.alive,
        explode_time = 0,
        lives = lives or STARTING_LIVES,

        isExploding = function(self)
            return self.status == statusEnum.exploding
        end,

        drawFlameThrust = function(self, fillType, color)
            love.graphics.setColor(color)

            local x, y, radius, flame = self.x, self.y, self.radius, self.thrust.flame
            local sin, cos = math.sin(self.angle), math.cos(self.angle)
            love.graphics.polygon(
                fillType,
                (x - (2/3 * cos + 0.5 * sin) * radius), (y + (2/3 * sin - 0.5 * cos) * radius),
                (x - radius * flame * cos),             (y + radius * flame * sin),
                (x - (2/3 * cos - 0.5 * sin) * radius), (y + (2/3 * sin + 0.5 * cos) * radius),
                (x - 1/2 * cos * radius),               (y + 1/2 * sin * radius)
            )
        end,

        drawShipShape = function (self, x, y, radius, angle, r, g, b, opacity)
            local sin, cos = math.sin(angle), math.cos(angle)

            love.graphics.setColor(r, g, b, opacity)
            love.graphics.polygon(
                "line",
                (x + 4/3 * cos * radius),         (y - 4/3 * sin * radius),
                (x - (2/3 * cos + sin) * radius), (y + (2/3 * sin - cos) * radius),
                (x - 1/2 * cos * radius),         (y + 1/2 * sin * radius),
                (x - (2/3 * cos - sin) * radius), (y + (2/3 * sin + cos) * radius)
            )
        end,

        draw = function(self, faded)
            local opacity = faded and 0.5 or 1

            if self.status == statusEnum.alive then
                if self.thrusting then
                    if not self.thrust.big_flame then
                        self.thrust.flame = self.thrust.flame - 10 * love.timer.getDelta()

                        if self.thrust.flame < 1.5 then
                            self.thrust.big_flame = true
                        end
                    else
                        self.thrust.flame = self.thrust.flame + 10 * love.timer.getDelta()

                        if self.thrust.flame > 2.5 then
                            self.thrust.big_flame = false
                        end
                    end

                    self:drawFlameThrust("fill", { 1, 0.7, 0.2 })
                    self:drawFlameThrust("line", { 1, 0.4, 0.1})
                end

                self:drawShipShape(self.x, self.y, self.radius, self.angle, 1, 1, 1, opacity)

                -- love.graphics.setColor(1, 1, 1, opacity)

                -- local x, y, radius = self.x, self.y, self.radius
                -- local sin, cos = math.sin(self.angle), math.cos(self.angle)
                -- love.graphics.polygon(
                --     "line",
                --     (x + 4/3 * cos * radius),         (y - 4/3 * sin * radius),
                --     (x - (2/3 * cos + sin) * radius), (y + (2/3 * sin - cos) * radius),
                --     (x - 1/2 * cos * radius),         (y + 1/2 * sin * radius),
                --     (x - (2/3 * cos - sin) * radius), (y + (2/3 * sin + cos) * radius)
                -- )
            elseif self.status == statusEnum.exploding then
                love.graphics.setColor(1, 0.2, 0.1, opacity)
                love.graphics.circle("fill", self.x, self.y, self.radius * 1.5)
                love.graphics.setColor(1, 0.5, 0.2, opacity)
                love.graphics.circle("fill", self.x, self.y, self.radius)
                love.graphics.setColor(1, 0.9, 0.2, opacity)
                love.graphics.circle("fill", self.x, self.y, self.radius * 0.5)
            end

            for _, laser in pairs(self.lasers) do
                laser:draw(faded)
            end

            if show_debugging then
                love.graphics.setColor(0, 1, 0, opacity)
                love.graphics.circle("fill", self.x, self.y, 1) --center
                love.graphics.circle("line", self.x, self.y, self.radius) --hitbox
            end
        end,

        drawLives = function(self, faded)
            local opacity = faded and 0.5 or 1
            local x_pos, x_offset, y_pos = 60, 20, 20
            if self.lives > 0 then
                for i = 1, self.lives - 1 do
                    self:drawShipShape(x_pos + x_offset * i, y_pos, self.radius / 2, VIEW_ANGLE, 0, 1, 0, opacity)
                end

                if self.status == statusEnum.exploding then
                    self:drawShipShape(x_pos + x_offset * self.lives, y_pos, self.radius / 2, VIEW_ANGLE, 0.8, 0, 0, opacity)
                elseif self.lives == 1 then
                    self:drawShipShape(x_pos + x_offset * self.lives, y_pos, self.radius / 2, VIEW_ANGLE, 0.8, 0.5, 0, opacity)
                else
                    self:drawShipShape(x_pos + x_offset * self.lives, y_pos, self.radius / 2, VIEW_ANGLE, 0, 1, 0, opacity)
                end
            end
        end,

        shoot = function(self)
            if #self.lasers < LASER_LIMIT and player.status == statusEnum.alive then
                table.insert(self.lasers, Laser(self.x, self.y, self.angle))
            end
        end,

        removeLaser = function(self, i)
            table.remove(self.lasers, i)
        end,

        move = function(self, dt)
            if self.status == statusEnum.alive then
                local friction = 0.7

                self.rotation = 2 * math.pi * dt

                if love.keyboard.isDown("a", "left", "kp4") then
                    self.angle = self.angle + self.rotation
                end

                if love.keyboard.isDown("d", "right", "kp6") then
                    self.angle = self.angle - self.rotation
                end

                if self.thrusting then
                    self.thrust.x = self.thrust.x + self.thrust.speed * math.cos(self.angle) * dt
                    self.thrust.y = self.thrust.y - self.thrust.speed * math.sin(self.angle) * dt
                elseif self.thrust.x ~= 0 or self.thrust.y ~= 0 then
                    self.thrust.x = self.thrust.x - friction * self.thrust.x * dt
                    self.thrust.y = self.thrust.y - friction * self.thrust.y * dt
                end

                self.x = self.x + self.thrust.x
                self.y = self.y + self.thrust.y

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
            elseif self.status == statusEnum.exploding then
                self.explode_time = self.explode_time + dt

                if self.explode_time > EXPLODE_DUR then
                    self:respawn()
                end
            end

            for i, laser in pairs(self.lasers) do
                laser:move(dt)

                if laser.travel_time > LASER_TIMER then
                    self:removeLaser(i)
                end

                if laser:doneExploding() then
                    self:removeLaser(i)
                end
            end
        end,

        respawn = function(self)
            self.lives = self.lives - 1
            if self.lives <= 0 then
                game:changeGameState("ended")
                return
            else
                self.status = statusEnum.alive
                self.explode_time = 0
                self.x = love.graphics.getWidth() / 2
                self.y = love.graphics.getHeight() / 2
            end
        end,

        explode = function(self)
            self.status = statusEnum.exploding
            self.thrust.x = 0
            self.thrust.y = 0
        end,
    }
end

return Player