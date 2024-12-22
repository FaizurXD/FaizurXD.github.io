class AdManager {

      constructor() {

        this.banner = document.querySelector('.ad-banner');

        this.retries = 0;

        this.maxRetries = 3;

        this.initialize();

      }



      async initialize() {

        try {

          await this.loadAd();

          this.setupMouseTracking();

          this.setupViewability();

        } catch (error) {

          console.error('Ad initialization failed:', error);

        }

      }



      async loadAd() {

        try {

          const response = await fetch('https://lunargen.onrender.com/etc/ads');

          if (!response.ok) throw new Error('Ad fetch failed');

          const data = await response.json();

          await this.renderAd(data);

          this.banner.classList.add('loaded');

          this.trackEvent('impression', data.id);

        } catch (error) {

          if (this.retries++ < this.maxRetries) {

            await new Promise(r => setTimeout(r, 2000));

            return this.loadAd();

          }

          this.banner.classList.add('error');

        }

      }



      async renderAd(data) {

        const img = new Image();

        await new Promise((resolve, reject) => {

          img.onload = resolve;

          img.onerror = reject;

          img.src = data.bannerUrl;

          img.alt = data.bannerAlt || 'Advertisement';

          img.classList.add('ad-image');

        });



        this.banner.appendChild(img);

        setTimeout(() => img.classList.add('loaded'), 0);

        

        if (data.clickUrl) {

          this.banner.style.cursor = 'pointer';

          this.banner.onclick = () => {

            this.trackEvent('click', data.id);

            window.open(data.clickUrl, '_blank', 'noopener,noreferrer');

          };

        }

      }



      setupMouseTracking() {

        this.banner.onmousemove = (e) => {

          const rect = this.banner.getBoundingClientRect();

          const x = ((e.clientX - rect.left) / rect.width) * 100;

          const y = ((e.clientY - rect.top) / rect.height) * 100;

          this.banner.style.setProperty('--mouse-x', `${x}%`);

          this.banner.style.setProperty('--mouse-y', `${y}%`);

        };

      }



      setupViewability() {

        new IntersectionObserver(

          (entries) => entries[0].isIntersecting && this.trackEvent('viewable'),

          { threshold: 0.5 }

        ).observe(this.banner);

      }



      async trackEvent(event, id = null) {

        try {

          const data = {

            event,

            id,

            timestamp: Date.now(),

            viewport: { width: innerWidth, height: innerHeght }

          };



          navigator.sendBeacon?.('https://lunargen.onrender.com/etc/analytics', 

            JSON.stringify(data)) || 

          await fetch('https://lunargen.onrender.com/etc/analytics', {

            method: 'POST',

            body: JSON.stringify(data),

            keepalive: true

          });

        } catch (error) {

          console.error('Analytics error:', error);

        }

      }

    }



    addEventListener('DOMContentLoaded', () => new AdManager());

