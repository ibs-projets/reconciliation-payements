$( function() {
	
	// Counters
	// $('.counter').countUp();


	// reveal items on scroll
	function reveal(){
		var reveals = document.querySelectorAll('.reveal');
	
		for(var i = 0; i < reveals.length; i++){
	
		var windowHeight = window.innerHeight;
		var cardTop = reveals[i].getBoundingClientRect().top;
		var cardRevealPoint = 150;
		
		if(cardTop < windowHeight - cardRevealPoint){
			reveals[i].classList.add('active');
		}
		else{
			reveals[i].classList.remove('active');
		}
		}
	}
	window.addEventListener('scroll', reveal);
	reveal();


	// LOADER
	$("#global-loader").fadeOut("slow");

	// PAGE LOADING
	$(window).on("load", function(e) {
		$("#global-loader").fadeOut("slow");
	})
	
	// BACK TO TOP BUTTON
	$(window).on("scroll", function(e) {
		if ($(this).scrollTop() > 130) {
			$('#back-to-top').removeClass('animate-reverse');
			$('#back-to-top').addClass('animate');
			$('#back-to-top').fadeIn('slow');
		} else {
			$('#back-to-top').removeClass('animate');
			$('#back-to-top').addClass('animate-reverse');
			$('#back-to-top').fadeOut('slow');
		}
	});

	// PROGRESS BAR ON SCROLL
	window.addEventListener('scroll', ()=>{
		var widnowScroll = document.body.scrollTop || document.documentElement.scrollTop,
		height = document.documentElement.scrollHeight - document.documentElement.clientHeight,
		scrollAmount = (widnowScroll / height) * 100;
		document.querySelector(".progress-top-bar").style.width = scrollAmount + "%";
	})

	// Landing Side Menu
	var landingSidemenu = $(".sidemenu-landing"),
		navHeader = $(".nav-header-main.sticky"),
		body = $("body"),
		navHeight;
	
	///Create a margin top to prevent content 'jumps':
	landingSidemenu.before('<div class="prevent-top"></div>');
	function preventTop() {
		navHeight = navHeader.innerHeight();
		landingSidemenu.css({"margin-top": + navHeight + "px"});
	};
	preventTop(); //Run.
	
	// Toggle Landing Page Sidemenu
	openLandingSidemenu = ()=>{
		$(body).toggleClass("landing-sidemenu-open");
	}

	// click outside of sidemenu to close
	$('.landing-page-content').on('click touchstart', function (event) {
		event.stopPropagation();
	
		// closing of sidebar menu when clicking outside of it
		if (!$(event.target).closest('#landingMenuBtn').length) {
			var sidebarTarg = $(event.target).closest('#landingMenuBtn').length;
			if (!sidebarTarg) {
				$('body').removeClass('landing-sidemenu-open');
			}
		}
	});

	// for menu scroll
	const pageLink = document.querySelectorAll(".nav-scroll");

	pageLink.forEach((elem) => {
		elem.addEventListener("click", (e) => {
			e.preventDefault();

			let WinUrl = window.location.pathname.split('/');
			if(WinUrl[WinUrl.length - 1] == 'landing.html'){
				window.location.assign(elem.getAttribute("href"))
			}

			let headerOffset = 55;
			let elemOffsetTop = document.querySelector(elem.getAttribute("href"))
			let elementPosition = elemOffsetTop.getBoundingClientRect().top - headerOffset;
			window.scrollBy(0, elementPosition); 
			
		});
	});

	// section menu active
	function onScroll(event) {
		const sections = document.querySelectorAll(".nav-scroll");
		const scrollPos = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;

		sections.forEach((ele,index)=> {
			const val = ele.getAttribute("href");
			const refElement = document.querySelector(val);
			const scrollTopMinus = scrollPos + 95;
			if (
				refElement.offsetTop <= scrollTopMinus &&
				refElement.offsetTop + refElement.offsetHeight > scrollTopMinus
			) {
				ele.classList.add("active");
			}
			else {
				ele.classList.remove("active");
			}
		})
	}
	window.document.addEventListener("scroll", onScroll);
});

