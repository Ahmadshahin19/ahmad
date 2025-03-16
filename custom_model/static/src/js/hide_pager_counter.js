/** @odoo-module **/
import { ListRenderer } from "@web/views/list/list_renderer";
import { FormRenderer } from "@web/views/form/form_renderer";
import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { patch } from 'web.utils';
import session from 'web.session';
var rpc = require('web.rpc');

function applyPagerPatch(Renderer) {
    patch(Renderer.prototype, 'partner_pager_patch', {
        setup() {
            this._super();

            // Define the custom style to hide the pager counter
            const styleId = 'custom-style';
            const existingStyleElement = document.getElementById(styleId);
            if (!existingStyleElement) {
                const style = document.createElement('style');
                style.id = styleId;
                style.textContent = `
                    .o_pager_counter {
                        display: none !important;
                    }
                `;
                document.head.appendChild(style);
            }

            // Prepare user data for the RPC call
            var userData = {
                userId: session.uid,
                viewId: this.env.config.viewId,
                externalModule: 'custom_model',  // استبدل بقيمة اسم المديول الخارجي للجروب
                externalId: 'pager_counter_show_in_contact',  // استبدل بقيمة الاسم المعرف الخارجي للجروب
            };

            // Make RPC call to check user permissions
            rpc.query({
                model: 'function.model',
                method: 'get_action_value',
                args: [userData.viewId, userData.userId, userData.externalModule, userData.externalId],
            }).then(function (response) {
                const existingStyleElement = document.getElementById(styleId);
                if (!response) {
                    if (existingStyleElement) {
                        document.head.removeChild(existingStyleElement);
                    }
                }
            }).catch(error => {
                console.error("Error processing data:", error);
            });
        }
    });
}

// Apply the patch to the List, Form, and Kanban renderers
applyPagerPatch(ListRenderer);
applyPagerPatch(FormRenderer);
applyPagerPatch(KanbanRenderer);