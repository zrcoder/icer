#!/usr/bin/env python3
"""
UI Effects System - Adds visual feedback and animations to ICER
"""

import pygame
from typing import Dict, List, Optional, Tuple
import random
import math


class Particle:
    """Simple particle for effects"""
    
    def __init__(self, x: float, y: float, vx: float = 0, vy: float = 0, 
                 color: Tuple[int, int, int] = (255, 255, 255), 
                 lifetime: float = 1.0, size: int = 3):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = size
    
    def update(self, dt: float) -> bool:
        """Update particle, return False if dead"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt  # Gravity
        self.lifetime -= dt
        
        return self.lifetime > 0
    
    def render(self, screen: pygame.Surface):
        """Render particle"""
        if self.lifetime <= 0:
            return
        
        # Fade out based on lifetime
        alpha = self.lifetime / self.max_lifetime
        color = tuple(int(c * alpha) for c in self.color)
        
        # Shrink as it dies
        size = int(self.size * alpha)
        if size > 0:
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), size)


class UIEffects:
    """Manages visual effects and UI animations"""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.particles: List[Particle] = []
        self.notifications: List[Dict] = []
        self.screen_shakes: List[Dict] = []
        
        # Animation timers
        self.flame_particles_timer = 0
        self.ice_shimmer_timer = 0
        
    def update(self, dt: float):
        """Update all effects"""
        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]
        
        # Update notifications
        self.notifications = [n for n in self.notifications if n['lifetime'] > 0]
        for notif in self.notifications:
            notif['lifetime'] -= dt
            notif['y'] -= 30 * dt  # Float upward
            
        # Update screen shakes
        self.screen_shakes = [s for s in self.screen_shakes if s['duration'] > 0]
        for shake in self.screen_shakes:
            shake['duration'] -= dt
            
        # Update animation timers
        self.flame_particles_timer += dt
        self.ice_shimmer_timer += dt
    
    def render(self, offset_x: int = 0, offset_y: int = 0):
        """Render all effects"""
        # Apply screen shake
        shake_offset_x, shake_offset_y = self.get_screen_shake()
        total_offset_x = offset_x + shake_offset_x
        total_offset_y = offset_y + shake_offset_y
        
        # Create temporary surface for effects with shake
        if shake_offset_x != 0 or shake_offset_y != 0:
            effects_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            effects_surface.fill((0, 0, 0, 0))
            self._render_particles(effects_surface, total_offset_x, total_offset_y)
            self._render_notifications(effects_surface, total_offset_x, total_offset_y)
            self.screen.blit(effects_surface, (0, 0))
        else:
            self._render_particles(self.screen, total_offset_x, total_offset_y)
            self._render_notifications(self.screen, total_offset_x, total_offset_y)
    
    def _render_particles(self, surface: pygame.Surface, offset_x: int, offset_y: int):
        """Render particles"""
        for particle in self.particles:
            # Apply screen shake offset
            particle.x += offset_x
            particle.y += offset_y
            particle.render(surface)
            # Remove the offset for next particle
            particle.x -= offset_x
            particle.y -= offset_y
    
    def _render_notifications(self, surface: pygame.Surface, offset_x: int, offset_y: int):
        """Render notifications"""
        for notif in self.notifications:
            alpha = min(1.0, notif['lifetime'])
            color = tuple(int(c * alpha) for c in notif['color'])
            
            font = pygame.font.Font(None, notif['size'])
            text = font.render(notif['text'], True, color)
            text_rect = text.get_rect(center=(notif['x'] + offset_x, notif['y'] + offset_y))
            
            # Add background
            padding = 10
            bg_rect = text_rect.inflate(padding * 2, padding)
            bg_color = (20, 20, 30, int(200 * alpha))
            
            # Create temporary surface for background with alpha
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill(bg_color)
            surface.blit(bg_surface, bg_rect.topleft)
            
            # Draw text
            surface.blit(text, text_rect)
    
    def add_particles(self, x: float, y: float, count: int, 
                     colors: List[Tuple[int, int, int]], 
                     speed: float = 100, spread: float = 90):
        """Add explosion particles"""
        for _ in range(count):
            angle = random.uniform(0, spread)
            velocity = random.uniform(speed * 0.5, speed)
            vx = velocity * math.cos(math.radians(angle))
            vy = -velocity * math.sin(math.radians(angle))
            
            color = random.choice(colors)
            size = random.randint(2, 6)
            lifetime = random.uniform(0.3, 1.2)
            
            self.particles.append(Particle(x, y, vx, vy, color, lifetime, size))
    
    def add_notification(self, text: str, x: float, y: float, 
                        color: Tuple[int, int, int] = (255, 255, 255),
                        size: int = 24, lifetime: float = 2.0):
        """Add floating notification"""
        self.notifications.append({
            'text': text,
            'x': x,
            'y': y,
            'color': color,
            'size': size,
            'lifetime': lifetime
        })
    
    def add_screen_shake(self, intensity: float = 10, duration: float = 0.3):
        """Add screen shake effect"""
        self.screen_shakes.append({
            'intensity': intensity,
            'duration': duration
        })
    
    def get_screen_shake(self) -> Tuple[int, int]:
        """Get current screen shake offset"""
        if not self.screen_shakes:
            return 0, 0
        
        shake = self.screen_shakes[0]
        intensity = shake['intensity'] * (shake['duration'] / 0.3)  # Fade out
        
        offset_x = random.uniform(-intensity, intensity)
        offset_y = random.uniform(-intensity, intensity)
        
        return int(offset_x), int(offset_y)
    
    def create_flame_extinguish_effect(self, x: int, y: int):
        """Create flame extinguish effect"""
        screen_x = x * 40 + 20  # Convert grid to screen coordinates
        screen_y = (15 - y) * 40 + 20
        
        # Steam particles (white/gray)
        self.add_particles(screen_x, screen_y, 15, 
                          [(255, 255, 255), (200, 200, 200), (150, 150, 150)],
                          speed=80, spread=120)
        
        # Add notification
        self.add_notification("EXTINGUISHED!", screen_x, screen_y - 30,
                             color=(100, 200, 255), size=20)
        
        # Small screen shake
        self.add_screen_shake(3, 0.2)
    
    def create_ice_melt_effect(self, x: int, y: int):
        """Create ice melting effect"""
        screen_x = x * 40 + 20
        screen_y = (15 - y) * 40 + 20
        
        # Water particles (blue)
        self.add_particles(screen_x, screen_y, 10,
                          [(100, 150, 255), (150, 200, 255), (200, 230, 255)],
                          speed=60, spread=100)
        
        # Add notification
        self.add_notification("MELTED!", screen_x, screen_y - 30,
                             color=(150, 200, 255), size=18)
    
    def create_ice_create_effect(self, x: int, y: int):
        """Create ice creation effect"""
        screen_x = x * 40 + 20
        screen_y = (15 - y) * 40 + 20
        
        # Ice crystals (light blue/white)
        self.add_particles(screen_x, screen_y, 8,
                          [(200, 230, 255), (180, 210, 255), (255, 255, 255)],
                          speed=40, spread=60)
        
        # Add notification
        self.add_notification("ICE CREATED!", screen_x, screen_y - 30,
                             color=(200, 230, 255), size=18)
    
    def create_pot_ignite_effect(self, x: int, y: int):
        """Create pot ignition effect"""
        screen_x = x * 40 + 20
        screen_y = (15 - y) * 40 + 20
        
        # Fire particles (orange/red)
        self.add_particles(screen_x, screen_y, 12,
                          [(255, 200, 100), (255, 150, 50), (255, 100, 0)],
                          speed=100, spread=80)
        
        # Add notification
        self.add_notification("IGNITED!", screen_x, screen_y - 30,
                             color=(255, 200, 100), size=20)
        
        # Screen shake
        self.add_screen_shake(5, 0.3)
    
    def create_portal_effect(self, x: int, y: int, entry: bool = True):
        """Create portal teleport effect"""
        screen_x = x * 40 + 20
        screen_y = (15 - y) * 40 + 20
        
        # Magic particles (purple/pink)
        self.add_particles(screen_x, screen_y, 20,
                          [(255, 100, 255), (200, 100, 255), (150, 100, 200)],
                          speed=150, spread=360)
        
        # Add notification
        text = "PORTAL EXIT!" if not entry else "PORTAL ENTER!"
        self.add_notification(text, screen_x, screen_y - 30,
                             color=(200, 100, 255), size=20)
        
        # Screen shake
        self.add_screen_shake(8, 0.4)