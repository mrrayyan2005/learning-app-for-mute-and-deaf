// Get the buttons and the website content container
const englishBtn = document.getElementById('english-btn');
const gujaratiBtn = document.getElementById('gujarati-btn');

// Define the English and Gujarati translations
const translations = {
  english: {
    logo: 'SignLearn',
    homeLink: 'Home',
    englishSignLink: 'English-Sign',
    gujaratiSignLink: 'Gujarati-Sign',
    loginLink: 'Login',
    signupLink: 'Sign Up',
    heading: 'Welcome to our website',
    paragraph: 'This is a sample paragraph.',
    alphabetBtn: 'Learn Alphabets',
    wordsBtn: 'Learn Greetings',
    aboutTitle: 'About Us',
    aboutParagraph: 'We provide resources and tools to help you master sign language and communicate effectively. Explore our learning materials and support for Deaf and Mute individuals.',
    quickLinksTitle: 'Quick Links',
    homeFooterLink: 'Home',
    aboutFooterLink: 'About Us',
    loginFooterLink: 'Login',
    signupFooterLink: 'Sign Up',
    contactTitle: 'Contact Us',
    contactEmail: 'Email: info@signlearn.com',
    contactPhone: 'Phone: +1 234 567 890',
    contactAddress: 'Address: Knowledge Park-2, Greater Noida',
    footerBottomText: '&copy; 2024 SignLearn. All Rights Reserved.'
  },
  gujarati: {
    logo: 'સાઇનલર્ન',
    homeLink: 'ઘર',
    englishSignLink: 'ઇંગલિશ-સાઇન',
    gujaratiSignLink: 'ગુજરાતી-સાઇન',
    loginLink: 'લૉગિન',
    signupLink: 'સાઇન અપ કરો',
    heading: 'આપણી વેબસાઇટમાં આવકારો',
    paragraph: 'આ એક નમૂના પેરાગ્રાફ છે.',
    alphabetBtn: 'Learn Alphabets',
    wordsBtn: 'Learn Greetings',
    aboutTitle: 'અમારા વિશે',
    aboutParagraph: 'અમે તમને સાઇન લૅંગ્વેજમાં પ્રભુત્વ મેળવવા અને અસરકારક રીતે સંચાર કરવામાં મદદ કરવા માટે સાધનો અને સાધનો પ્રદાન કરીએ છીએ. અમારા શીખવાની સામગ્રી અને Deaf અને Mute વ્યક્તિઓ માટે સહાયકોની શોધ કરો.',
    quickLinksTitle: 'ઝડપી કડીઓ',
    homeFooterLink: 'ઘર',
    aboutFooterLink: 'અમારા વિશે',
    loginFooterLink: 'લૉગિન',
    signupFooterLink: 'સાઇન અપ કરો',
    contactTitle: 'સંપર્ક કરો',
    contactEmail: 'ઇમેલ: info@signlearn.com',
    contactPhone: 'ફોન: +1 234 567 890',
    contactAddress: 'સરનામું: નોલેજ પાર્ક-2, ગ્રેટર નોઈડા',
    footerBottomText: '&copy; 2024 સાઇનલર્ન. બધી હકો અધિકૃત છે.'
  }
};

// Function to change the language
function changeLanguage(language) {
  const translation = translations[language];

  document.getElementById('logo').textContent = translation.logo;
  document.getElementById('home-link').textContent = translation.homeLink;
  document.getElementById('english-sign-link').textContent = translation.englishSignLink;
  document.getElementById('gujarati-sign-link').textContent = translation.gujaratiSignLink;
  document.getElementById('login-link').textContent = translation.loginLink;
  document.getElementById('signup-link').textContent = translation.signupLink;
  document.getElementById('heading').textContent = translation.heading;
  document.getElementById('paragraph').textContent = translation.paragraph;
  document.getElementById('alphabet-btn').textContent = translation.alphabetBtn;
  document.getElementById('words-btn').textContent = translation.wordsBtn;
  document.getElementById('about-title').textContent = translation.aboutTitle;
  document.getElementById('about-paragraph').textContent = translation.aboutParagraph;
  document.getElementById('quick-links-title').textContent = translation.quickLinksTitle;
  document.getElementById('home-footer-link').textContent = translation.homeFooterLink;
  document.getElementById('about-footer-link').textContent = translation.aboutFooterLink;
  document.getElementById('login-footer-link').textContent = translation.loginFooterLink;
  document.getElementById('signup-footer-link').textContent = translation.signupFooterLink;
  document.getElementById('contact-title').textContent = translation.contactTitle;
  document.getElementById('contact-email').textContent = translation.contactEmail;
  document.getElementById('contact-phone').textContent = translation.contactPhone;
  document.getElementById('contact-address').textContent = translation.contactAddress;
  document.getElementById('footer-bottom-text').innerHTML = translation.footerBottomText;
}

// Add event listeners to the buttons
englishBtn.addEventListener('click', () => changeLanguage('english'));
gujaratiBtn.addEventListener('click', () => changeLanguage('gujarati'));



document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('alphabet-btn').addEventListener('click', function() {
        fetch('/learn-alphabets', {
            method: 'POST'
        })
        .then(response => {
            if (response.redirected) {
                // Redirect to the new page
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            // Handle any additional data if needed
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred.');
        });
    });

    document.getElementById('words-btn').addEventListener('click', function() {
        fetch('/learn-words', {
            method: 'POST'
        })
        .then(response => {
            if (response.redirected) {
                // Redirect to the new page
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            // Handle any additional data if needed
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred.');
        });
    });
});
