import routes from '@/router/routes';
import EmployeeNavbar from '@/components/employee/EmployeeNavbar';

import { createRouter, createWebHistory } from 'vue-router';
import { shallowMount, RouterLinkStub } from '@vue/test-utils';


const router = createRouter({
    routes,
    history: createWebHistory()
});

const mountSettings = {
    propsData: {
        page: 'favourites',
        //numNotifs: 3
    },
    attachTo: document.body,
    global: {
        plugins: [router],
        stubs: {
            stubs: ['faIcon'],
            RouterLink: RouterLinkStub
        }
    }
};

describe('EmployeeNavbar.vue', () => {
    let wrapper;

    beforeEach(() => {
        // render navbar
        wrapper = shallowMount(EmployeeNavbar, mountSettings);
    });

    it('highlights the correct navbar link as the active page', () => {
        // check that the home link is highlighted        
        const favouritesLink = wrapper.findAll('.navbar-link').at(1);
        expect(favouritesLink.classes()).toContain('navbar-active-link');
    });

    /*it('renders number of notifications when component is created', () => {
        // check that the number of notifs is correct
        const notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.text()).toBe('3');
    });

    it('shows the notification bubble if there is notif >= 1', () => {
        const notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.exists()).toBe(true);
    });

    it('hides the notification bubble if there is notif < 1', async () => {
        mountSettings.propsData.numNotifs = 0;
        wrapper = shallowMount(EmployeeNavbar, mountSettings);
        
        const notifBubble = wrapper.find('#navbar-notif-alert');
        expect(notifBubble.exists()).toBe(false);
    });*/
});